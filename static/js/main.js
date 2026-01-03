/**
 * ADHD Screening System - Main JavaScript
 * Utility functions and helpers
 */

// API call wrapper
async function apiCall(url, method='GET', data=null) {
    const opts = {method, headers:{'Content-Type':'application/json'}};
    if(data) opts.body = JSON.stringify(data);
    const res = await fetch(url, opts);
    if(!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
}

// Show notification
function notify(msg, type='info') {
    const div = document.createElement('div');
    div.textContent = msg;
    div.style.cssText = `position:fixed;top:20px;right:20px;padding:15px;border-radius:8px;background:${type==='error'?'#f56565':'#48bb78'};color:white;z-index:1000`;
    document.body.appendChild(div);
    setTimeout(()=>div.remove(), 3000);
}

// Session storage helpers
const Session = {
    get: (key) => sessionStorage.getItem(key),
    set: (key, val) => sessionStorage.setItem(key, val),
    clear: () => sessionStorage.clear()
};

console.log('ADHD Screening System loaded');
