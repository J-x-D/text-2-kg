/**
 * Get the backend URL dynamically based on the environment
 * In production (GitHub Codespaces), it derives the URL from window.location
 * In development, it uses localhost
 */
export function getBackendUrl(): string {
  // If NEXT_PUBLIC_BACKEND_URL is explicitly set and not undefined, use it
  if (process.env.NEXT_PUBLIC_BACKEND_URL && process.env.NEXT_PUBLIC_BACKEND_URL !== 'undefined') {
    return process.env.NEXT_PUBLIC_BACKEND_URL;
  }

  // In browser environment, derive from current URL
  if (typeof window !== 'undefined') {
    const currentUrl = window.location.origin;
    
    // Check if we're in GitHub Codespaces
    if (currentUrl.includes('github.dev') || currentUrl.includes('githubpreview.dev')) {
      // Replace port 3000 with 8000 for backend
      return currentUrl.replace('-3000.', '-8000.');
    }
    
    // For localhost or other environments
    if (currentUrl.includes('localhost') || currentUrl.includes('127.0.0.1')) {
      return currentUrl.replace(':3000', ':8000');
    }
  }

  // Fallback to localhost
  return 'http://localhost:8000';
}
