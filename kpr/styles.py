"""Complete CSS stylesheet for the KPR (Keepers) website."""


def get_css() -> str:
    return '''
/* ==========================================================================
   KPR — KEEPERS WEBSITE CSS
   Complete production stylesheet
   ========================================================================== */

/* ---------------------------------------------------------------------------
   GOOGLE FONTS
   --------------------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ---------------------------------------------------------------------------
   CSS CUSTOM PROPERTIES
   --------------------------------------------------------------------------- */
:root {
  --menu-height: 5rem;
  --menu-width: 7rem;
  --menu-pad: 2rem;
  --menu-radius: 2rem;
  --line-thickness: 1px;
  --line-light: rgba(255, 255, 255, 0.15);
  --line-dark: rgba(0, 0, 0, 0.15);
  --colorLines: var(--line-light);
  --z-frame: 10;
  --z-menu: 20;
  --z-loader: 100;
  --z-console: 50;
  --z-footer: 5;
  --z-resize-overlays: 200;
  --padding: 2rem;
  --accent: #c0fb50;
}

/* ---------------------------------------------------------------------------
   RESET & BASE
   --------------------------------------------------------------------------- */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 62.5%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', sans-serif;
  font-size: 1.6rem;
  line-height: 1.5;
  color: #fff;
  background: #000;
  overflow-x: hidden;
  min-height: 100vh;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  border: none;
  background: none;
  cursor: pointer;
  color: inherit;
  font-family: inherit;
}

img {
  max-width: 100%;
  display: block;
}

ul, ol {
  list-style: none;
}

/* ---------------------------------------------------------------------------
   TYPOGRAPHY
   --------------------------------------------------------------------------- */

/* Display / Section Headings */
.heading-display,
.section-title,
h1.heading-display,
h2.section-title {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  letter-spacing: -0.07em;
  line-height: 0.9;
  text-transform: uppercase;
  font-size: 5rem;
}

@media (min-width: 768px) {
  .heading-display,
  .section-title,
  h1.heading-display,
  h2.section-title {
    font-size: 6rem;
  }
}

.heading-display--large {
  font-size: 6rem;
  line-height: 0.85;
}

@media (min-width: 768px) {
  .heading-display--large {
    font-size: 9rem;
  }
}

/* UI / Mono Typography */
.ui-text,
.mono-text,
.label-text {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
}

.ui-text--md {
  font-size: 1.2rem;
  font-weight: 450;
  letter-spacing: -0.03em;
}

.ui-text--lg {
  font-size: 1.3rem;
  font-weight: 450;
  letter-spacing: -0.04em;
}

/* Body Typography */
.body-text {
  font-family: 'Inter', sans-serif;
  font-size: 1.6rem;
  line-height: 1.5;
}

.body-text--sm {
  font-size: 1.4rem;
  line-height: 1.4;
}

.body-text--lg {
  font-size: 1.8rem;
  line-height: 1.7;
}

/* Muted */
.text-muted {
  opacity: 0.4;
}

/* Console color */
.text-console {
  color: #8ca6ff;
}

/* ---------------------------------------------------------------------------
   PRELOADER
   --------------------------------------------------------------------------- */
.preloader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-loader);
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: opacity 0.6s ease, visibility 0.6s ease;
}

.preloader.is-hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.preloader__bar-track {
  width: 18rem;
  height: 0.1rem;
  background: #e1e1e1;
  position: relative;
  overflow: hidden;
  border-radius: 1px;
}

@media (min-width: 768px) {
  .preloader__bar-track {
    width: 87rem;
  }
}

.preloader__bar-fill {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000;
  transform-origin: left center;
  transform: scaleX(0);
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.preloader__label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  color: #000;
  margin-top: 1.6rem;
}

/* ---------------------------------------------------------------------------
   FRAME SYSTEM (Fixed Chrome)
   --------------------------------------------------------------------------- */
.the-frame {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: var(--z-frame);
}

.the-frame--light {
  --colorLines: var(--line-dark);
  color: #000;
}

.the-frame--dark {
  --colorLines: var(--line-light);
  color: #fff;
}

/* Top Bar */
.the-frame__top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--menu-height);
  display: flex;
  align-items: center;
  border-bottom: var(--line-thickness) solid var(--colorLines);
}

.the-frame__top-left {
  width: var(--menu-width);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: var(--line-thickness) solid var(--colorLines);
  pointer-events: auto;
  cursor: pointer;
  flex-shrink: 0;
}

.the-frame__top-center {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.the-frame__top-right {
  width: var(--menu-width);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: var(--line-thickness) solid var(--colorLines);
  flex-shrink: 0;
}

/* Progress Bar in top center */
.the-frame__progress {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.4;
}

/* Submenu in top center */
.the-frame__submenu {
  display: flex;
  align-items: center;
  gap: 2rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  pointer-events: auto;
}

.the-frame__submenu a,
.the-frame__submenu button {
  opacity: 0.4;
  transition: opacity 0.3s ease;
  pointer-events: auto;
}

.the-frame__submenu a:hover,
.the-frame__submenu button:hover,
.the-frame__submenu a.is-active,
.the-frame__submenu button.is-active {
  opacity: 1;
}

/* Left Sidebar — desktop only */
.the-frame__left {
  display: none;
}

@media (min-width: 768px) {
  .the-frame__left {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: absolute;
    top: var(--menu-height);
    left: 0;
    width: var(--menu-width);
    height: calc(100% - var(--menu-height));
    border-right: var(--line-thickness) solid var(--colorLines);
  }
}

.the-frame__left-top {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  pointer-events: auto;
}

.the-frame__left-top svg {
  width: 2.4rem;
  height: 2.4rem;
}

.the-frame__left-bottom {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.6rem;
  padding-bottom: 2rem;
  pointer-events: auto;
}

.the-frame__left-bottom button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.6rem;
  height: 3.6rem;
  border-radius: 50%;
  transition: background 0.3s ease, color 0.3s ease;
  pointer-events: auto;
}

.the-frame__left-bottom button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.the-frame__left-bottom button svg {
  width: 1.8rem;
  height: 1.8rem;
}

/* Right Sidebar (mirrors left if needed) */
.the-frame__right {
  display: none;
}

/* Hamburger button */
.hamburger-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  pointer-events: auto;
  cursor: pointer;
  background: none;
  border: none;
  color: inherit;
  position: relative;
}

.hamburger-btn svg {
  width: 2.7rem;
  height: 0.6rem;
}

/* Frame border radius helpers */
.the-frame__corner-tl {
  border-top-left-radius: var(--menu-radius);
}

.the-frame__corner-tr {
  border-top-right-radius: var(--menu-radius);
}

.the-frame__corner-bl {
  border-bottom-left-radius: var(--menu-radius);
}

.the-frame__corner-br {
  border-bottom-right-radius: var(--menu-radius);
}

/* ---------------------------------------------------------------------------
   NAVIGATION MENU (Fullscreen Overlay)
   --------------------------------------------------------------------------- */
.nav-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-menu);
  display: flex;
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.4s ease, visibility 0.4s ease;
}

.nav-menu.is-open {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.nav-menu__backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
}

.nav-menu__panel {
  position: relative;
  width: 100%;
  max-width: 60rem;
  height: 100%;
  background: #000;
  border-radius: 0 var(--menu-radius) var(--menu-radius) 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  transform: translateX(-100%);
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-menu.is-open .nav-menu__panel {
  transform: translateX(0);
}

@media (min-width: 768px) {
  .nav-menu__panel {
    border-radius: var(--menu-radius) 0 0 var(--menu-radius);
  }
}

/* Menu header with close button */
.nav-menu__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--menu-height);
  padding: 0 var(--padding);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}

.nav-menu__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  color: #fff;
  cursor: pointer;
}

.nav-menu__close svg {
  width: 2rem;
  height: 2rem;
}

/* Nav Items */
.nav-menu__list {
  padding: 3rem var(--padding);
  flex: 1;
}

.nav-menu__item {
  display: block;
  width: 100%;
}

.nav-menu__link {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 4rem;
  font-weight: 650;
  text-transform: uppercase;
  letter-spacing: -0.05em;
  line-height: 1.1;
  padding: 1.2rem 2rem;
  border-radius: 1rem;
  color: #fff;
  transition: background 0.25s ease, color 0.25s ease;
  cursor: pointer;
}

@media (min-width: 768px) {
  .nav-menu__link {
    font-size: 6.4rem;
    padding: 1.4rem 2.4rem;
    border-radius: 1.2rem;
  }
}

.nav-menu__link:hover {
  background: #fff;
  color: #000;
}

.nav-menu__link.is-active {
  background: var(--accent);
  color: #000;
}

/* Menu sections / dividers */
.nav-menu__divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
  margin: 2rem 0;
}

/* Menu footer */
.nav-menu__footer {
  padding: 2rem var(--padding);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  gap: 2rem;
  flex-shrink: 0;
}

.nav-menu__footer-link {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  color: #fff;
  opacity: 0.4;
  transition: opacity 0.3s ease;
}

.nav-menu__footer-link:hover {
  opacity: 1;
}

/* ---------------------------------------------------------------------------
   SECTIONS
   --------------------------------------------------------------------------- */
.section {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
}

.section--light {
  background: #fff;
  color: #000;
  --colorLines: var(--line-dark);
}

.section--dark {
  background: #000;
  color: #fff;
  --colorLines: var(--line-light);
}

.section__inner {
  position: relative;
  width: 100%;
  min-height: 100vh;
  padding: var(--menu-height) var(--padding) var(--padding);
}

@media (min-width: 768px) {
  .section__inner {
    padding-left: calc(var(--menu-width) + var(--padding));
    padding-right: var(--padding);
  }
}

/* Section grid layouts */
.section__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--padding);
  width: 100%;
}

@media (min-width: 768px) {
  .section__grid--2col {
    grid-template-columns: 1fr 1fr;
  }

  .section__grid--3col {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .section__grid--4col {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }

  .section__grid--sidebar {
    grid-template-columns: 1fr 2fr;
  }

  .section__grid--sidebar-right {
    grid-template-columns: 2fr 1fr;
  }
}

/* Section separator lines */
.section__line {
  width: 100%;
  height: var(--line-thickness);
  background: var(--colorLines);
}

.section__line--vertical {
  width: var(--line-thickness);
  height: 100%;
  background: var(--colorLines);
}

/* ---------------------------------------------------------------------------
   HERO SECTION
   --------------------------------------------------------------------------- */
.hero {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
}

.hero__bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    180deg,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.3) 60%,
    rgba(0, 0, 0, 0.8) 100%
  );
  z-index: 1;
}

.hero__content {
  position: relative;
  z-index: 2;
  padding: var(--padding);
  padding-bottom: 6rem;
}

@media (min-width: 768px) {
  .hero__content {
    padding-left: calc(var(--menu-width) + var(--padding));
    padding-bottom: 8rem;
  }
}

.hero__title {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  letter-spacing: -0.07em;
  line-height: 0.85;
  text-transform: uppercase;
  font-size: 5rem;
  color: #fff;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .hero__title {
    font-size: 10rem;
  }
}

@media (min-width: 1200px) {
  .hero__title {
    font-size: 14rem;
  }
}

.hero__subtitle {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  color: #fff;
  opacity: 0.4;
  margin-bottom: 3rem;
}

/* ---------------------------------------------------------------------------
   SCROLL INDICATOR
   --------------------------------------------------------------------------- */
.scroll-indicator {
  position: fixed;
  bottom: 3rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  z-index: var(--z-frame);
  pointer-events: none;
  animation: pulse 2.5s ease-in-out infinite;
}

.scroll-indicator__label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1rem;
  font-weight: 400;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.5;
}

.scroll-indicator__arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 2s ease-in-out infinite;
}

.scroll-indicator__arrow svg {
  width: 2rem;
  height: 2rem;
  opacity: 0.5;
}

.scroll-indicator.is-hidden {
  opacity: 0;
  transition: opacity 0.5s ease;
  pointer-events: none;
}

/* ---------------------------------------------------------------------------
   COLLECTION GALLERY — 3D Card Stacking
   --------------------------------------------------------------------------- */
.collection-gallery {
  position: relative;
  width: 100%;
  min-height: 100vh;
  perspective: 1200px;
  overflow: hidden;
}

.collection-gallery__container {
  position: relative;
  width: 100%;
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collection-gallery__card {
  position: absolute;
  width: 28rem;
  height: 36rem;
  border-radius: 1.6rem;
  overflow: hidden;
  transition: transform 0.8s cubic-bezier(0.22, 1, 0.36, 1),
              opacity 0.6s ease;
  will-change: transform;
  backface-visibility: hidden;
}

@media (min-width: 768px) {
  .collection-gallery__card {
    width: 34rem;
    height: 44rem;
  }
}

.collection-gallery__card:nth-child(1) {
  transform: translate3d(0, 0, 0) rotateY(0deg);
  z-index: 5;
}

.collection-gallery__card:nth-child(2) {
  transform: translate3d(6rem, -2rem, -5rem) rotateY(-5deg);
  z-index: 4;
  opacity: 0.85;
}

.collection-gallery__card:nth-child(3) {
  transform: translate3d(12rem, -4rem, -10rem) rotateY(-10deg);
  z-index: 3;
  opacity: 0.7;
}

.collection-gallery__card:nth-child(4) {
  transform: translate3d(-6rem, -2rem, -5rem) rotateY(5deg);
  z-index: 4;
  opacity: 0.85;
}

.collection-gallery__card:nth-child(5) {
  transform: translate3d(-12rem, -4rem, -10rem) rotateY(10deg);
  z-index: 3;
  opacity: 0.7;
}

.collection-gallery__card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.collection-gallery__card-label {
  position: absolute;
  bottom: 1.6rem;
  left: 1.6rem;
  right: 1.6rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  color: #fff;
  opacity: 0.7;
}

.collection-gallery__info {
  padding: var(--padding);
  text-align: center;
}

@media (min-width: 768px) {
  .collection-gallery__info {
    padding-left: calc(var(--menu-width) + var(--padding));
  }
}

/* ---------------------------------------------------------------------------
   TABLEAU SECTIONS — Sticky Pinned Layers
   --------------------------------------------------------------------------- */
.tableau {
  position: relative;
  width: 100%;
}

.tableau__sticky {
  position: sticky;
  top: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.tableau__layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  will-change: transform, opacity;
  transition: transform 1s cubic-bezier(0.22, 1, 0.36, 1),
              opacity 0.8s ease;
}

.tableau__layer--origin-tl {
  transform-origin: top left;
}

.tableau__layer--origin-tr {
  transform-origin: top right;
}

.tableau__layer--origin-bl {
  transform-origin: bottom left;
}

.tableau__layer--origin-br {
  transform-origin: bottom right;
}

.tableau__layer--origin-center {
  transform-origin: center center;
}

.tableau__layer img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tableau__content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--padding);
  z-index: 2;
}

@media (min-width: 768px) {
  .tableau__content {
    padding-left: calc(var(--menu-width) + var(--padding));
  }
}

/* Hold button with crosshair */
.tableau__hold-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  cursor: pointer;
  pointer-events: auto;
}

.tableau__hold-btn svg {
  width: 4rem;
  height: 4rem;
  animation: pulse 2s ease-in-out infinite;
}

.tableau__hold-btn-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.6;
}

/* ---------------------------------------------------------------------------
   FOOTER
   --------------------------------------------------------------------------- */
.footer {
  position: relative;
  width: 100%;
  background: #000;
  color: #fff;
  z-index: var(--z-footer);
  --colorLines: var(--line-light);
}

.footer__main {
  display: grid;
  grid-template-columns: 1fr;
  min-height: 35rem;
  border-top: 1px solid #333;
}

@media (min-width: 768px) {
  .footer__main {
    grid-template-columns: repeat(4, 1fr);
  }
}

.footer__col {
  padding: var(--padding);
  border-right: 1px solid #333;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.footer__col:last-child {
  border-right: none;
}

@media (max-width: 767px) {
  .footer__col {
    border-right: none;
    border-bottom: 1px solid #333;
  }
  .footer__col:last-child {
    border-bottom: none;
  }
}

.footer__col-title {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.4;
  margin-bottom: 2rem;
}

.footer__links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer__link {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  transition: opacity 0.3s ease;
  opacity: 0.7;
}

.footer__link:hover {
  opacity: 1;
}

/* Footer wordmark / logo area */
.footer__wordmark {
  position: relative;
  width: 100%;
  overflow: hidden;
  padding: 4rem var(--padding);
  border-top: 1px solid #333;
}

.footer__wordmark-inner {
  position: relative;
  overflow: hidden;
}

.footer__wordmark svg {
  width: 100%;
  max-width: 80rem;
  height: auto;
}

.footer__wordmark-parallax {
  will-change: transform;
  transition: transform 0.1s linear;
}

/* Bottom bar */
.footer__bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.6rem var(--padding);
  border-top: 1px solid #333;
  flex-wrap: wrap;
  gap: 1rem;
}

@media (min-width: 768px) {
  .footer__bottom {
    padding-left: calc(var(--menu-width) + var(--padding));
  }
}

.footer__legal {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.footer__legal-link {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.3;
  transition: opacity 0.3s ease;
}

.footer__legal-link:hover {
  opacity: 0.7;
}

.footer__copyright {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.3;
}

/* ---------------------------------------------------------------------------
   CONSOLE OVERLAY
   --------------------------------------------------------------------------- */
.console-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-console);
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.4s ease, visibility 0.4s ease;
}

.console-overlay.is-open {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.console-overlay__backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
}

.console-overlay__panel {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: calc(var(--menu-height) + var(--padding)) var(--padding) var(--padding);
}

@media (min-width: 768px) {
  .console-overlay__panel {
    padding-left: calc(var(--menu-width) + var(--padding));
  }
}

.console-overlay__bg-shape {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: 60%;
  opacity: 0.08;
}

.console-overlay__bg-shape svg {
  width: 100%;
  height: 100%;
  stroke: #8ca6ff;
  stroke-width: 0.5;
  fill: none;
}

.console-overlay__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-shrink: 0;
}

.console-overlay__title {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  color: #8ca6ff;
}

.console-overlay__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.2rem;
  height: 3.2rem;
  color: #8ca6ff;
  cursor: pointer;
  pointer-events: auto;
}

.console-overlay__body {
  flex: 1;
  overflow-y: auto;
  position: relative;
}

.console-overlay__line {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  font-feature-settings: 'zero' on;
  color: #8ca6ff;
  line-height: 1.8;
  opacity: 0.7;
}

.console-overlay__line--highlight {
  opacity: 1;
  color: #8ca6ff;
}

.console-overlay__line--muted {
  opacity: 0.3;
}

/* Console input */
.console-overlay__input-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-top: 1.6rem;
  flex-shrink: 0;
  border-top: 1px solid rgba(140, 166, 255, 0.15);
  padding-top: 1.2rem;
}

.console-overlay__prompt {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  font-feature-settings: 'zero' on;
  color: #8ca6ff;
  flex-shrink: 0;
}

.console-overlay__cursor {
  display: inline-block;
  width: 0.8rem;
  height: 1.6rem;
  background: #8ca6ff;
  animation: cursorBlink 1s step-end infinite;
}

/* ---------------------------------------------------------------------------
   HACKY TEXT ANIMATION
   --------------------------------------------------------------------------- */
.hacky-text {
  position: relative;
  display: inline-block;
}

.hacky-text .spacer {
  visibility: hidden;
  display: inline-block;
  white-space: pre;
}

.hacky-text .animation {
  position: absolute;
  top: 0;
  left: 0;
  display: inline-block;
  white-space: pre;
  overflow: hidden;
}

/* ---------------------------------------------------------------------------
   DOT CAPTION ANIMATION
   --------------------------------------------------------------------------- */
.dot-caption {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
}

.dot-caption__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: currentColor;
  opacity: 0;
  transition: opacity 0.4s ease;
  flex-shrink: 0;
}

.dot-caption__dot.is-visible {
  opacity: 1;
}

.dot-caption__char {
  display: inline-block;
  opacity: 0;
  transform: translateY(0.4rem);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dot-caption__char.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* ---------------------------------------------------------------------------
   LINK HOVER — Underline slide-in from left
   --------------------------------------------------------------------------- */
.link-hover {
  position: relative;
  display: inline-block;
}

.link-hover::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.link-hover:hover::after {
  transform: scaleX(1);
}

/* ---------------------------------------------------------------------------
   JS LINE — Scroll reveal
   --------------------------------------------------------------------------- */
.js-line {
  opacity: 0;
  transform: translateY(2rem);
  transition: opacity 0.8s cubic-bezier(0.22, 1, 0.36, 1),
              transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.js-line.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger delay classes */
.js-line--delay-1 { transition-delay: 0.1s; }
.js-line--delay-2 { transition-delay: 0.2s; }
.js-line--delay-3 { transition-delay: 0.3s; }
.js-line--delay-4 { transition-delay: 0.4s; }
.js-line--delay-5 { transition-delay: 0.5s; }
.js-line--delay-6 { transition-delay: 0.6s; }
.js-line--delay-7 { transition-delay: 0.7s; }
.js-line--delay-8 { transition-delay: 0.8s; }

/* ---------------------------------------------------------------------------
   AUDIO BUTTON — Animated Bars
   --------------------------------------------------------------------------- */
.audio-btn {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 2px;
  width: 2.4rem;
  height: 1.6rem;
  cursor: pointer;
  pointer-events: auto;
}

.audio-btn__bar {
  width: 2px;
  background: currentColor;
  border-radius: 1px;
  transform-origin: bottom center;
  transition: transform 0.15s ease;
}

.audio-btn__bar:nth-child(1) {
  height: 40%;
  animation: audioBar1 1.2s ease-in-out infinite;
}

.audio-btn__bar:nth-child(2) {
  height: 70%;
  animation: audioBar2 1.0s ease-in-out infinite 0.1s;
}

.audio-btn__bar:nth-child(3) {
  height: 100%;
  animation: audioBar3 0.9s ease-in-out infinite 0.2s;
}

.audio-btn__bar:nth-child(4) {
  height: 55%;
  animation: audioBar4 1.1s ease-in-out infinite 0.15s;
}

.audio-btn__bar:nth-child(5) {
  height: 30%;
  animation: audioBar5 1.3s ease-in-out infinite 0.05s;
}

.audio-btn.is-paused .audio-btn__bar {
  animation-play-state: paused;
}

@keyframes audioBar1 {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1.0); }
}

@keyframes audioBar2 {
  0%, 100% { transform: scaleY(0.7); }
  50% { transform: scaleY(0.3); }
}

@keyframes audioBar3 {
  0%, 100% { transform: scaleY(1.0); }
  50% { transform: scaleY(0.5); }
}

@keyframes audioBar4 {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(0.9); }
}

@keyframes audioBar5 {
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(0.8); }
}

/* ---------------------------------------------------------------------------
   KEYFRAME ANIMATIONS
   --------------------------------------------------------------------------- */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(3rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-3rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

@keyframes cursorBlink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(0.6rem);
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* ---------------------------------------------------------------------------
   UTILITY ANIMATION CLASSES
   --------------------------------------------------------------------------- */
.anim-fade-in {
  animation: fadeIn 0.6s ease forwards;
}

.anim-slide-up {
  animation: slideUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.anim-slide-down {
  animation: slideDown 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.anim-scale-in {
  animation: scaleIn 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.anim-pulse {
  animation: pulse 2.5s ease-in-out infinite;
}

.anim-shimmer {
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s linear infinite;
}

/* ---------------------------------------------------------------------------
   CARD COMPONENT
   --------------------------------------------------------------------------- */
.card {
  position: relative;
  border-radius: 1.6rem;
  overflow: hidden;
  border: var(--line-thickness) solid var(--colorLines);
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
              border-color 0.3s ease;
}

.card:hover {
  transform: translateY(-0.4rem);
  border-color: rgba(255, 255, 255, 0.3);
}

.section--light .card:hover {
  border-color: rgba(0, 0, 0, 0.3);
}

.card__image {
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
}

.card__body {
  padding: 1.6rem;
}

.card__title {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 1.6rem;
  letter-spacing: -0.03em;
  margin-bottom: 0.4rem;
}

.card__meta {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.4;
}

/* ---------------------------------------------------------------------------
   BUTTON COMPONENTS
   --------------------------------------------------------------------------- */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 500;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  padding: 1.2rem 2.4rem;
  border-radius: 10rem;
  border: 1px solid var(--colorLines);
  cursor: pointer;
  transition: background 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.btn--primary {
  background: #fff;
  color: #000;
  border-color: #fff;
}

.btn--primary:hover {
  background: var(--accent);
  border-color: var(--accent);
}

.btn--outline {
  background: transparent;
  color: inherit;
}

.btn--outline:hover {
  background: rgba(255, 255, 255, 0.1);
}

.section--light .btn--outline:hover {
  background: rgba(0, 0, 0, 0.05);
}

.btn--accent {
  background: var(--accent);
  color: #000;
  border-color: var(--accent);
}

.btn--accent:hover {
  background: #d4ff7a;
  border-color: #d4ff7a;
}

.btn svg {
  width: 1.4rem;
  height: 1.4rem;
}

/* ---------------------------------------------------------------------------
   TAG / BADGE
   --------------------------------------------------------------------------- */
.tag {
  display: inline-flex;
  align-items: center;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  padding: 0.4rem 1rem;
  border-radius: 10rem;
  border: 1px solid var(--colorLines);
}

.tag--accent {
  background: var(--accent);
  color: #000;
  border-color: var(--accent);
}

/* ---------------------------------------------------------------------------
   IMAGE GALLERY / MEDIA
   --------------------------------------------------------------------------- */
.media-frame {
  position: relative;
  overflow: hidden;
  border-radius: var(--menu-radius);
  border: var(--line-thickness) solid var(--colorLines);
}

.media-frame img,
.media-frame video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-frame__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-frame__play {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 6rem;
  height: 6rem;
  color: #fff;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.media-frame__play:hover {
  transform: scale(1.1);
}

.media-frame__play svg {
  width: 6rem;
  height: 6rem;
}

/* ---------------------------------------------------------------------------
   STAT BLOCK
   --------------------------------------------------------------------------- */
.stat-block {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.stat-block__value {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 3.6rem;
  letter-spacing: -0.05em;
  line-height: 1;
}

.stat-block__label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  opacity: 0.4;
}

/* ---------------------------------------------------------------------------
   MARQUEE / TICKER
   --------------------------------------------------------------------------- */
.marquee {
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  border-top: var(--line-thickness) solid var(--colorLines);
  border-bottom: var(--line-thickness) solid var(--colorLines);
  padding: 1.2rem 0;
}

.marquee__inner {
  display: inline-flex;
  animation: marqueeScroll 20s linear infinite;
}

.marquee__item {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 2.4rem;
  letter-spacing: -0.05em;
  text-transform: uppercase;
  padding: 0 2rem;
  white-space: nowrap;
}

.marquee__item::after {
  content: '\\2022';
  margin-left: 2rem;
  opacity: 0.3;
}

@keyframes marqueeScroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

/* ---------------------------------------------------------------------------
   MOBILE NAVIGATION
   --------------------------------------------------------------------------- */
@media (max-width: 767px) {
  .the-frame__top {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: var(--z-frame);
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .the-frame__top-left {
    width: var(--menu-height);
    border-right: var(--line-thickness) solid var(--colorLines);
  }

  .the-frame__top-right {
    width: var(--menu-height);
    border-left: var(--line-thickness) solid var(--colorLines);
  }

  .section__inner {
    padding-top: calc(var(--menu-height) + var(--padding));
  }
}

/* Mobile subnav — fixed bottom */
.mobile-subnav {
  display: none;
}

@media (max-width: 767px) {
  .mobile-subnav {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: var(--menu-height);
    z-index: var(--z-frame);
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: var(--line-thickness) solid var(--colorLines);
    align-items: center;
    justify-content: center;
    gap: 3rem;
    pointer-events: auto;
  }

  .mobile-subnav a,
  .mobile-subnav button {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 400;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    font-feature-settings: 'zero' on;
    opacity: 0.4;
    transition: opacity 0.3s ease;
    pointer-events: auto;
    color: #fff;
  }

  .mobile-subnav a:hover,
  .mobile-subnav button:hover,
  .mobile-subnav a.is-active,
  .mobile-subnav button.is-active {
    opacity: 1;
  }
}

/* ---------------------------------------------------------------------------
   RESIZE OVERLAYS
   --------------------------------------------------------------------------- */
.resize-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-resize-overlays);
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.resize-overlay.is-visible {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.resize-overlay__message {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-feature-settings: 'zero' on;
  text-align: center;
}

/* ---------------------------------------------------------------------------
   ADDITIONAL LAYOUT UTILITIES
   --------------------------------------------------------------------------- */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.flex-col {
  display: flex;
  flex-direction: column;
}

.gap-sm { gap: 0.8rem; }
.gap-md { gap: 1.6rem; }
.gap-lg { gap: 3.2rem; }
.gap-xl { gap: 6.4rem; }

.mt-auto { margin-top: auto; }
.mb-auto { margin-bottom: auto; }
.ml-auto { margin-left: auto; }
.mr-auto { margin-right: auto; }

.w-full { width: 100%; }
.h-full { height: 100%; }
.h-screen { min-height: 100vh; }

.overflow-hidden { overflow: hidden; }
.relative { position: relative; }

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* ---------------------------------------------------------------------------
   SCROLLBAR STYLING
   --------------------------------------------------------------------------- */
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Console scrollbar */
.console-overlay__body::-webkit-scrollbar-thumb {
  background: rgba(140, 166, 255, 0.2);
}

.console-overlay__body::-webkit-scrollbar-thumb:hover {
  background: rgba(140, 166, 255, 0.4);
}

/* ---------------------------------------------------------------------------
   SELECTION HIGHLIGHT
   --------------------------------------------------------------------------- */
::selection {
  background: var(--accent);
  color: #000;
}

::-moz-selection {
  background: var(--accent);
  color: #000;
}

/* ---------------------------------------------------------------------------
   STREAMLIT OVERRIDES
   --------------------------------------------------------------------------- */
.stApp {
  background: #000 !important;
}

.stApp > header {
  display: none !important;
}

.stApp [data-testid="stToolbar"] {
  display: none !important;
}

.stApp [data-testid="stDecoration"] {
  display: none !important;
}

.stApp [data-testid="stStatusWidget"] {
  display: none !important;
}

.stApp footer {
  display: none !important;
}

.stApp .main .block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

iframe[title="streamlit_kpr_component"] {
  border: none !important;
}
'''
