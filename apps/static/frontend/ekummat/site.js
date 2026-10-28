(() => {
  'use strict';

  document.documentElement.classList.add('js');
  const one = (selector, root = document) => root.querySelector(selector);
  const all = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const readPreference = (key) => {
    try { return localStorage.getItem(`ekummat.${key}`); } catch (_) { return null; }
  };
  const savePreference = (key, value) => {
    try { localStorage.setItem(`ekummat.${key}`, value); return true; } catch (_) { return false; }
  };
  let toastTimer;
  const notify = (message) => {
    const toast = one('[data-toast]');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('visible'), 4000);
  };

  const menuButton = one('[data-menu-toggle]');
  const menu = one('#site-navigation');
  const closeMenu = () => {
    if (!menuButton || !menu) return;
    menu.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
  };
  menuButton?.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  all('a', menu || document.createElement('div')).forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.classList.contains('is-open')) {
      closeMenu();
      menuButton.focus();
    }
  });
  all('[data-about-link]').forEach(link => link.addEventListener('click', () => {
    const about = one('#about');
    if (about) about.open = true;
  }));
  if (location.hash === '#about' && one('#about')) one('#about').open = true;

  const chapterSearch = one('[data-chapter-search]');
  const chapterCards = all('[data-chapter-card]');
  let chapterFilter = 'all';
  let chaptersExpanded = false;
  const expandButton = one('[data-expand-chapters]');
  const normalize = (value) => value.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f\u064b-\u065f\u0670]/g, '').replace(/[’'\-]/g, '').replace(/\s+/g, ' ').trim();
  const filterChapters = () => {
    const query = normalize(chapterSearch?.value || '');
    let matching = 0;
    let visible = 0;
    const filtered = Boolean(query) || chapterFilter !== 'all';
    chapterCards.forEach(card => {
      const matchingName = normalize(card.dataset.name).includes(query);
      const matchingPlace = chapterFilter === 'all' || card.dataset.place === chapterFilter;
      const matches = matchingName && matchingPlace;
      if (matches) matching += 1;
      card.hidden = !matches || (!filtered && !chaptersExpanded && matching > 12);
      if (!card.hidden) visible += 1;
    });
    const count = one('[data-chapter-count]');
    if (count) count.textContent = filtered ? `${matching} ${matching === 1 ? 'Surah' : 'Surahs'} found` : `Showing ${visible} of ${chapterCards.length} Surahs`;
    const empty = one('[data-no-chapters]');
    if (empty) empty.hidden = visible > 0 || chapterCards.length === 0;
    if (expandButton) {
      expandButton.hidden = filtered || chapterCards.length <= 12;
      expandButton.textContent = chaptersExpanded ? 'Show fewer Surahs ↑' : `View all ${chapterCards.length} Surahs ↓`;
      expandButton.setAttribute('aria-expanded', String(chaptersExpanded));
    }
  };
  if (chapterCards.length) filterChapters();
  expandButton?.addEventListener('click', () => {
    chaptersExpanded = !chaptersExpanded;
    filterChapters();
    if (!chaptersExpanded) one('#quran').scrollIntoView({ block: 'start' });
  });
  chapterSearch?.addEventListener('input', filterChapters);
  all('[data-chapter-filter]').forEach(button => button.addEventListener('click', () => {
    chapterFilter = button.dataset.chapterFilter;
    all('[data-chapter-filter]').forEach(item => {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    filterChapters();
  }));
  one('[data-reset-chapters]')?.addEventListener('click', () => {
    chapterSearch.value = '';
    one('[data-chapter-filter="all"]').click();
    chapterSearch.focus();
  });
  document.addEventListener('keydown', event => {
    const editing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if (event.key === '/' && !editing && chapterSearch && !event.metaKey && !event.ctrlKey) {
      event.preventDefault();
      chapterSearch.focus();
    }
  });

  let savedPlace = null;
  try {
    const parsed = JSON.parse(readPreference('reading-place'));
    if (parsed && Number.isInteger(parsed.id) && parsed.id >= 1 && parsed.id <= 114 && typeof parsed.title === 'string') savedPlace = parsed;
  } catch (_) { /* Ignore an unavailable or outdated preference. */ }
  const continueLink = one('[data-continue-reading]');
  if (continueLink && savedPlace) {
    continueLink.href = `/${savedPlace.id}/`;
    one('[data-continue-title]', continueLink).textContent = savedPlace.title;
    continueLink.hidden = false;
  }

  const reader = one('[data-reader]');
  if (reader) {
    const storedSize = Number(readPreference('text-size'));
    let fontSize = storedSize >= 16 && storedSize <= 28 ? storedSize : 20;
    const updateFont = () => {
      reader.style.setProperty('--reading-size', `${fontSize}px`);
      all('[data-font-size]', reader).forEach(label => { label.textContent = fontSize; });
      all('[data-font-change]', reader).forEach(button => {
        button.disabled = Number(button.dataset.fontChange) < 0 ? fontSize <= 16 : fontSize >= 28;
      });
    };
    all('[data-font-change]', reader).forEach(button => button.addEventListener('click', () => {
      fontSize = Math.max(16, Math.min(28, fontSize + Number(button.dataset.fontChange) * 2));
      updateFont();
      savePreference('text-size', String(fontSize));
    }));
    updateFont();
    const themeButton = one('[data-reading-theme]', reader);
    const setNight = (night) => {
      reader.classList.toggle('reader--night', night);
      themeButton?.setAttribute('aria-pressed', String(night));
      const label = themeButton && one('span', themeButton);
      if (label) label.textContent = night ? 'Day reading' : 'Night reading';
    };
    setNight(readPreference('reading-theme') === 'night');
    themeButton?.addEventListener('click', () => {
      const night = !reader.classList.contains('reader--night');
      setNight(night);
      savePreference('reading-theme', night ? 'night' : 'day');
    });
    const saveButton = one('[data-save-reading]', reader);
    if (saveButton) {
      const sameChapter = savedPlace?.id === Number(saveButton.dataset.chapterId);
      saveButton.setAttribute('aria-pressed', String(sameChapter));
      if (sameChapter) one('[data-save-label]', saveButton).textContent = 'Place saved';
      saveButton.addEventListener('click', () => {
        const place = { id: Number(saveButton.dataset.chapterId), title: saveButton.dataset.chapterTitle };
        if (savePreference('reading-place', JSON.stringify(place))) {
          saveButton.setAttribute('aria-pressed', 'true');
          one('[data-save-label]', saveButton).textContent = 'Place saved';
          notify('Surah saved. Continue from the homepage on this browser.');
        } else notify('Your browser could not save this place. You can bookmark this page instead.');
      });
    }
  }

  all('[data-hadith]').forEach(card => {
    const tabs = all('[data-language-tab]', card);
    const panels = all('[data-language-panel]', card);
    const activate = (tab) => {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      panels.forEach(panel => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) {
          event.preventDefault();
          activate(tabs[next]);
          tabs[next].focus();
        }
      });
    });
    if (tabs.length) activate(tabs[0]);
  });

  const copyText = async (text) => {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      try { await navigator.clipboard.writeText(text); return; } catch (_) { /* Try the selection fallback. */ }
    }
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.style.cssText = 'position:fixed;left:-9999px;top:0';
    const previousFocus = document.activeElement;
    document.body.appendChild(field);
    field.select();
    let copied = false;
    try { copied = document.execCommand('copy'); } finally { field.remove(); previousFocus?.focus(); }
    if (!copied) throw new Error('Clipboard unavailable');
  };
  all('[data-copy-hadith]').forEach(button => button.addEventListener('click', async () => {
    const card = button.closest('[data-hadith]');
    const panel = all('[data-language-panel]', card).find(item => !item.hidden);
    const content = panel && one('.hadith-content', panel);
    const reference = one('[data-reference]', card);
    if (!content) return;
    try {
      await copyText(`${content.textContent.trim()}\n\n${reference?.textContent.trim() || ''}`);
      notify('Hadith and reference copied.');
    } catch (_) { notify('Copy is unavailable. Please select the text and copy it.'); }
  }));
  all('[data-share-url]').forEach(button => button.addEventListener('click', async () => {
    const url = new URL(button.dataset.shareUrl, location.origin).href;
    try {
      if (navigator.share) await navigator.share({ title: 'Hadith · Ekummat', url });
      else { await copyText(url); notify('Hadith link copied.'); }
    } catch (error) { if (error.name !== 'AbortError') notify('Sharing is unavailable. Open the Hadith link to share it.'); }
  }));
})();
