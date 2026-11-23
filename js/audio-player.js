/**
 * Audio Player for TOEIC Listening 300
 * Plays audio segments, handles pauses, rate toggling (1.0x / 0.85x),
 * turn seeking via startMs/endMs, and provides Web Speech API fallback.
 */

export class AudioPlayer {
  constructor() {
    this.audio = new Audio();
    this.playbackRate = 1.0;
    this.isPlaying = false;
    this.activeSegments = [];
    this.currentSegmentIndex = 0;
    this.onStateChange = null;
    this.turnTimer = null;

    this.audio.addEventListener('play', () => {
      this.isPlaying = true;
      this.notify();
    });

    this.audio.addEventListener('pause', () => {
      this.isPlaying = false;
      this.notify();
    });

    this.audio.addEventListener('ended', () => {
      this.handleSegmentEnded();
    });

    this.audio.addEventListener('error', (e) => {
      console.warn('Audio element error, falling back to speech synthesis if possible:', e);
      this.fallbackSpeech();
    });
  }

  setRate(rate) {
    this.playbackRate = rate;
    this.audio.playbackRate = rate;
    this.notify();
  }

  notify() {
    if (typeof this.onStateChange === 'function') {
      this.onStateChange({
        isPlaying: this.isPlaying,
        playbackRate: this.playbackRate
      });
    }
  }

  stop() {
    clearTimeout(this.turnTimer);
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    this.audio.pause();
    this.audio.currentTime = 0;
    this.activeSegments = [];
    this.currentSegmentIndex = 0;
    this.isPlaying = false;
    this.notify();
  }

  /**
   * Play multiple audio segments sequentially (e.g. Part 1 or Part 2 statements)
   */
  playSegments(segments, optionOrder = null) {
    this.stop();
    if (!segments || segments.length === 0) return;

    let ordered = [...segments];
    if (optionOrder && optionOrder.length > 0) {
      // Reorder segments matching optionOrder for choice items
      const questionSegs = ordered.filter(s => !s.choiceId);
      const choiceSegs = ordered.filter(s => !!s.choiceId);
      const sortedChoices = [];
      for (const choiceId of optionOrder) {
        const found = choiceSegs.find(s => s.choiceId === choiceId);
        if (found) sortedChoices.push(found);
      }
      ordered = [...questionSegs, ...sortedChoices];
    }

    this.activeSegments = ordered;
    this.currentSegmentIndex = 0;
    this.playCurrentSegment();
  }

  playCurrentSegment() {
    if (this.currentSegmentIndex >= this.activeSegments.length) {
      this.isPlaying = false;
      this.notify();
      return;
    }

    const seg = this.activeSegments[this.currentSegmentIndex];
    this.audio.src = seg.file;
    this.audio.playbackRate = this.playbackRate;

    this.audio.play().catch(err => {
      console.warn('Auto/manual play prevented or file missing, using speech fallback:', err);
      this.fallbackSpeech(seg.text, () => {
        this.handleSegmentEnded();
      });
    });
  }

  handleSegmentEnded() {
    const seg = this.activeSegments[this.currentSegmentIndex];
    const pause = (seg && seg.pauseAfterMs) ? seg.pauseAfterMs : 400;

    this.currentSegmentIndex++;
    if (this.currentSegmentIndex < this.activeSegments.length) {
      this.turnTimer = setTimeout(() => {
        this.playCurrentSegment();
      }, pause);
    } else {
      this.isPlaying = false;
      this.notify();
    }
  }

  /**
   * Play a group audio file, optionally seeking to a turn segment
   */
  playGroup(audioFile, startMs = 0, endMs = null, fallbackText = "") {
    this.stop();
    this.audio.src = audioFile;
    this.audio.playbackRate = this.playbackRate;

    const onLoaded = () => {
      this.audio.removeEventListener('loadedmetadata', onLoaded);
      if (startMs > 0) {
        this.audio.currentTime = startMs / 1000;
      }
      this.audio.play().catch(err => {
        console.warn('Group audio playback failed, falling back:', err);
        if (fallbackText) this.fallbackSpeech(fallbackText);
      });

      if (endMs && endMs > startMs) {
        const durationMs = (endMs - startMs) / this.playbackRate;
        this.turnTimer = setTimeout(() => {
          this.audio.pause();
          this.isPlaying = false;
          this.notify();
        }, durationMs);
      }
    };

    if (this.audio.readyState >= 1) {
      onLoaded();
    } else {
      this.audio.addEventListener('loadedmetadata', onLoaded);
      this.audio.load();
    }
  }

  playWord(text) {
    this.stop();
    this.fallbackSpeech(text);
  }

  playComparisonPair(textA, textB) {
    this.stop();
    this.fallbackSpeech(textA, () => {
      this.turnTimer = setTimeout(() => {
        this.fallbackSpeech(textB);
      }, 500);
    });
  }

  fallbackSpeech(text = "", onDone = null) {
    if (!('speechSynthesis' in window)) {
      if (onDone) onDone();
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = this.playbackRate === 0.85 ? 0.85 : 1.0;

    this.isPlaying = true;
    this.notify();

    utterance.onend = () => {
      this.isPlaying = false;
      this.notify();
      if (onDone) onDone();
    };
    utterance.onerror = () => {
      this.isPlaying = false;
      this.notify();
      if (onDone) onDone();
    };

    window.speechSynthesis.speak(utterance);
  }
}

export const audioPlayer = new AudioPlayer();
