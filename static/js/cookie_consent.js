/**
 * Cookie Consent Manager — Vinaigre du Maroc
 * Handles display, saving, and enforcement of cookie preferences.
 */
const CookieConsent = (function() {
    const COOKIE_NAME = 'vdm_cookie_consent';
    const EXPIRATION_DAYS = 365;
    const DEFAULT_CONSENT = { necessary: true, analytics: false, marketing: false, preferences: false, timestamp: null };
    let els = {};

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = `; expires=${date.toUTCString()}`;
        }
        document.cookie = `${name}=${value}${expires}; path=/; SameSite=Lax`;
    }

    function getConsentState() {
        const cookieStr = getCookie(COOKIE_NAME);
        if (cookieStr) {
            try { return JSON.parse(decodeURIComponent(cookieStr)); }
            catch (e) { console.error("Cookie consent parse error", e); }
        }
        return null;
    }

    function saveConsentState(state) {
        state.timestamp = new Date().toISOString();
        setCookie(COOKIE_NAME, encodeURIComponent(JSON.stringify(state)), EXPIRATION_DAYS);
        window.dispatchEvent(new CustomEvent('cookieConsentUpdated', { detail: state }));
        hideBanner(); hideModal(); showFloatingBtn();
    }

    function applyConsent(state) {
        if (!state) return;
        if (state.analytics) { /* Load analytics if enabled */ }
        if (state.marketing) { /* Load marketing scripts if enabled */ }
    }

    function showBanner()     { if (els.banner) els.banner.classList.add('cc-active'); if (els.floatingBtn) els.floatingBtn.classList.remove('cc-active'); }
    function hideBanner()     { if (els.banner) els.banner.classList.remove('cc-active'); }
    function showModal()      { if (els.modalOverlay) { els.modalOverlay.classList.add('cc-active'); const s = getConsentState() || DEFAULT_CONSENT; if (els.toggleAnalytics) els.toggleAnalytics.checked = s.analytics; if (els.toggleMarketing) els.toggleMarketing.checked = s.marketing; if (els.togglePreferences) els.togglePreferences.checked = s.preferences; } }
    function hideModal()      { if (els.modalOverlay) els.modalOverlay.classList.remove('cc-active'); }
    function showFloatingBtn() { if (els.floatingBtn) els.floatingBtn.classList.add('cc-active'); }

    function attachEvents() {
        if (els.btnAcceptAll) els.btnAcceptAll.addEventListener('click', function() { var s = { necessary:true, analytics:true, marketing:true, preferences:true }; saveConsentState(s); applyConsent(s); });
        if (els.btnRejectAll) els.btnRejectAll.addEventListener('click', function() { var s = { necessary:true, analytics:false, marketing:false, preferences:false }; saveConsentState(s); applyConsent(s); });
        if (els.btnCustomize) els.btnCustomize.addEventListener('click', showModal);
        if (els.modalClose) els.modalClose.addEventListener('click', hideModal);
        if (els.btnSavePreferences) els.btnSavePreferences.addEventListener('click', function() { var s = { necessary:true, analytics: els.toggleAnalytics ? els.toggleAnalytics.checked : false, marketing: els.toggleMarketing ? els.toggleMarketing.checked : false, preferences: els.togglePreferences ? els.togglePreferences.checked : false }; saveConsentState(s); applyConsent(s); });
        if (els.floatingBtn) els.floatingBtn.addEventListener('click', showModal);
        if (els.modalOverlay) els.modalOverlay.addEventListener('click', function(e) { if (e.target === els.modalOverlay) hideModal(); });
    }

    function init() {
        els = {
            banner: document.getElementById('cc-banner'),
            btnAcceptAll: document.getElementById('cc-btn-accept-all'),
            btnRejectAll: document.getElementById('cc-btn-reject-all'),
            btnCustomize: document.getElementById('cc-btn-customize'),
            modalOverlay: document.getElementById('cc-modal-overlay'),
            modalClose: document.getElementById('cc-modal-close'),
            btnSavePreferences: document.getElementById('cc-btn-save-preferences'),
            toggleAnalytics: document.getElementById('cc-toggle-analytics'),
            toggleMarketing: document.getElementById('cc-toggle-marketing'),
            togglePreferences: document.getElementById('cc-toggle-preferences'),
            floatingBtn: document.getElementById('cc-floating-btn')
        };
        var currentState = getConsentState();
        if (!currentState) { setTimeout(showBanner, 500); }
        else { applyConsent(currentState); showFloatingBtn(); }
        attachEvents();
    }

    return { init: init, getState: getConsentState, showPreferences: showModal };
})();

document.addEventListener('DOMContentLoaded', CookieConsent.init);
