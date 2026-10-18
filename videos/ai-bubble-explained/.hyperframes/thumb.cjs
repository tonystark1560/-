const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto('file://' + process.cwd() + '/thumb_tmp.html'); await p.waitForTimeout(500);
await p.screenshot({ path: 'renders/thumbnail.png' }); await b.close(); })();
