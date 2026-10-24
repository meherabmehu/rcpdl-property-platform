(() => {
    'use strict';
    const stage = document.querySelector('#media-stage');
    if (!stage) return;
    const $ = s => document.querySelector(s);
    const $$ = s => [...document.querySelectorAll(s)];
    const target = $('#panorama'), loading = $('.panorama-loading');
    // Query within the stage: the standalone reference error screen has no viewer.
    const fallback = stage.querySelector('.media-fallback');
    const poster = stage.querySelector('img');
    let viewer, timer, mode, generation = 0;
    const fail = message => {
        clearTimeout(timer); loading.hidden = true; fallback.hidden = false;
        fallback.querySelector('p').textContent = message;
    };
    const load = () => {
        const current = ++generation;
        clearTimeout(timer); viewer?.destroy(); viewer = null; window.rcPanorama = null;
        loading.hidden = false; fallback.hidden = true;
        if (mode !== 'panorama') {
            loading.hidden = true; return;
        }
        try {
            viewer = pannellum.viewer('panorama', {
                type: 'equirectangular', panorama: stage.dataset.panorama,
                autoLoad: true, showControls: false, showFullscreenCtrl: false,
                hfov: 100, minHfov: 45, maxHfov: 120, yaw: 0, pitch: 0,
                compass: false, mouseZoom: 'fullscreen', keyboardZoom: true,
                friction: 0.2, disableKeyboardCtrl: false,
            });
            window.rcPanorama = viewer;
            viewer.on('load', () => { if (current !== generation) return; clearTimeout(timer); loading.hidden = true; fallback.hidden = true; });
            viewer.on('error', () => { if (current === generation) fail('The panorama could not load. Check your connection or graphics support, then retry.'); });
            timer = setTimeout(() => fail('The panorama is taking too long to load. Please retry.'), 20000);
        } catch { fail('Your browser could not start the 360° viewer. Please retry or view photos.'); }
    };
    const setMode = value => {
        mode = value === 'video' ? 'video' : 'panorama';
        const panorama = mode === 'panorama';
        target.hidden = !panorama; poster.hidden = panorama;
        $$('.panorama-controls,.panorama-hint,.photo-alternative').forEach(x => x.hidden = !panorama);
        $$('.stage-play,.video-controls,.video-description').forEach(x => x.hidden = panorama);
        $$('.image-label', stage).forEach(x => x.textContent = panorama ? 'Illustrative panorama' : 'Illustrative image');
        $$('[data-mode]').forEach(b => { b.classList.toggle('outline', b.dataset.mode !== mode); b.setAttribute('aria-pressed', String(b.dataset.mode === mode)); });
        const url = new URL(location.href); url.searchParams.set('mode', mode); history.replaceState({}, '', url);
        load();
    };
    $$('[data-mode]').forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));
    const unavailableVideo = () => fail('No walkthrough video has been supplied. The 360° view and project photos are available.');
    $('.retry-media').addEventListener('click', () => mode === 'video' ? unavailableVideo() : load());
    $$('.stage-play,[data-media-fallback]').forEach(b => b.addEventListener('click', unavailableVideo));
    $('.video-controls input')?.addEventListener('input', unavailableVideo);
    $$('[data-zoom]').forEach(b => b.addEventListener('click', () => viewer?.setHfov(viewer.getHfov() + Number(b.dataset.zoom), 200)));
    $('[data-reset]').addEventListener('click', () => { viewer?.setYaw(0, 200); viewer?.setPitch(0, 200); viewer?.setHfov(100, 200); });
    $('.panorama-hint').addEventListener('click', () => target.focus());
    $('#visit-project').addEventListener('change', e => { const url = new URL(location.href); url.searchParams.set('project', e.target.value); location.href = url; });
    $$('.fullscreen-toggle').forEach(b => b.addEventListener('click', async () => {
        try { if (document.fullscreenElement) await document.exitFullscreen(); else await stage.requestFullscreen(); }
        catch { window.rcDemo.toast('Fullscreen is unavailable in this browser.'); }
    }));
    document.addEventListener('fullscreenchange', () => {
        $('.stage-top .fullscreen-toggle').textContent = document.fullscreenElement ? '⛶ Exit fullscreen' : '⛶ Fullscreen';
        viewer?.resize();
    });
    window.addEventListener('pagehide', () => { clearTimeout(timer); viewer?.destroy(); });
    window.addEventListener('pageshow', event => { if (event.persisted) load(); });
    setMode(new URLSearchParams(location.search).get('mode'));
})();
