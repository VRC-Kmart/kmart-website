/**
 * Simple router function to change the browser's location
 * @param {string} path - The path to navigate to
 * @returns {string} - The path that was navigated to
 */
function Router(path) {
    if (path === undefined || path === null) {
        return '/'; // something happened or someone called without path
    }
    window.location.href = path;
    return path; // return the path for chaining if needed
}
