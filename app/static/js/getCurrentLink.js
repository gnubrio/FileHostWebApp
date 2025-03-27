function copyURL() {
    const currentUrl = window.location.href;
    navigator.clipboard.writeText(currentUrl);
}
