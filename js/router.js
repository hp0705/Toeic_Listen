/**
 * Hash Router for TOEIC Listening 300
 */

export class Router {
  constructor() {
    this.routes = new Map();
    this.currentRoute = null;

    window.addEventListener('hashchange', () => this.handleRoute());
  }

  addRoute(pattern, handler) {
    this.routes.set(pattern, handler);
  }

  navigate(path) {
    window.location.hash = path;
  }

  handleRoute() {
    const rawHash = window.location.hash.slice(1) || '/dashboard';
    const [pathPart, queryPart] = rawHash.split('?');
    const params = new URLSearchParams(queryPart || '');

    for (const [pattern, handler] of this.routes.entries()) {
      const match = this.matchPattern(pattern, pathPart);
      if (match) {
        this.currentRoute = pathPart;
        handler(match.params, params);
        return;
      }
    }

    // Default route fallback
    if (this.routes.has('/dashboard')) {
      this.navigate('/dashboard');
    }
  }

  matchPattern(pattern, path) {
    const patternSegments = pattern.split('/').filter(Boolean);
    const pathSegments = path.split('/').filter(Boolean);

    if (patternSegments.length !== pathSegments.length) return null;

    const params = {};
    for (let i = 0; i < patternSegments.length; i++) {
      const p = patternSegments[i];
      const actual = pathSegments[i];
      if (p.startsWith(':')) {
        params[p.slice(1)] = decodeURIComponent(actual);
      } else if (p !== actual) {
        return null;
      }
    }
    return { params };
  }
}
