from app.domain.models.login_model import Session, Login
import json
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, Page
from services.logger import logger


def apply_stealth(page: Page):
    page.add_init_script(
        """
    // Remover navigator.webdriver
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

    // Adicionar plugins falsos
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
    });

    // Adicionar idiomas
    Object.defineProperty(navigator, 'languages', {
        get: () => ['pt-BR', 'pt'],
    });

    // Simular chrome runtime
    window.chrome = {
        runtime: {},
        loadTimes: () => {},
        csi: () => {},
    };

    // WebGL Vendor spoofing
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Intel Inc.';
        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
        return getParameter(parameter);
    };
    """
    )


def inject_session(page: Page, session: Session):
    page.add_init_script(
        f"""() => {{
            const data = {json.dumps(session.local_storage)};
            for (const [key, value] of Object.entries(data)) {{
                localStorage.setItem(key, value);
            }}
        }}"""
    )

    page.add_init_script(
        f"""() => {{
            const data = {json.dumps(session.session_storage)};
            for (const [key, value] of Object.entries(data)) {{
                sessionStorage.setItem(key, value);
            }}
        }}"""
    )


def get_login_session(login: Login) -> Session:
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1,
            is_mobile=False,
            has_touch=False,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )
        logger.info("Iniciando navegador")
        page = context.new_page()
        apply_stealth(page)
        breakpoint()
        page.goto("https://www.google.com/search?q=youtube")

        page.wait_for_timeout(2000)
        # <a jsname="UWckNb" class="zReHs" href="https://www.youtube.com/" data-ved="2ahUKEwjr4Ny40ZiSAxVNzTgGHcooPV8QFnoECAsQAQ" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;opi=89978449&amp;url=https://www.youtube.com/&amp;ved=2ahUKEwjr4Ny40ZiSAxVNzTgGHcooPV8QFnoECAsQAQ"><h3 class="LC20lb MBeuO DKV0Md" id="_Ca5uaau4Gc2a4-EPytH0-QU_40">YouTube</h3><br><div class="notranslate ESMNde HGLrXd ojE3Fb"><div class="q0vns"><span class="H9lube"><div class="eqA2re NjwKYd Vwoesf" aria-hidden="true"><img class="XNo5Ab" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABJklEQVR4Ae2WpVaFQRSFcaeS4QVwIjTiLbgk7D1w9xeg4FQcOu6acHeXtNnDmsFd7in/WetLI+f7dbYDAFEsAUvgoeAQ5k5iSQFpIH1kkMyQFXJMTsgpwTuc6jlHes2M3qNP71mge7g76DLNg8gygZ1QckGmuSdZJ7Azq8RDCSQTCJGgBCoFBWqVQLegQJcSmPnWIr9oICMXcIr4C4FJJbD9rUX+NtzX+CIQlfVbgS0lcP4jAVNt/UCA7acCZ0oAPxfQdXMLFNUBvpHflvgbAVM7h0B6zrfeD3kB+Ucg/xLKf4biPyLJX3GH9GFUogRSBQUSTSBZEwskQpFs1USyl6E0gRSRJtJPhsnci1B69oVQeqzXzOo9+kmj3juBeDw2BkSxBCyBO+9s03HRLVCoAAAAAElFTkSuQmCC" style="height:18px;width:18px" alt="" data-csiid="Ca5uaau4Gc2a4-EPytH0-QU_2" data-atf="1"></div></span><div class="CA5RN"><div><span class="VuuXrf">YouTube</span></div><div class="byrV5b"><cite class="tjvcx GvPZzd dTxz9 cHaqb" role="text">https://www.youtube.com</cite></div></div></div></div></a>
        page.click('a[href="https://www.youtube.com/"]')
        page.wait_for_timeout(1000)
        page.click('a:has-text("Fazer login")')
        page.wait_for_timeout(2000)

        page.wait_for_selector('input[type="email"]')
        page.fill('input[type="email"]', login.email)
        page.click('button:has-text("Avançar")')
        page.wait_for_timeout(2000)
        page.screenshot(path='./salvar.jpeg')
        page.wait_for_selector('input[type="password"]', timeout=15000)
        page.fill('input[type="password"]', login.password)
        page.click('button:has-text("Avançar")')
        page.wait_for_timeout(5000)

        state = context.storage_state()
        cookies = context.cookies()
        local_storage = page.evaluate("() => JSON.stringify(window.localStorage)")
        session_storage = page.evaluate("() => JSON.stringify(window.sessionStorage)")

        session = Session(
            state=state,
            cookies=cookies,
            local_storage=json.loads(local_storage),
            session_storage=json.loads(session_storage),
            expire_at=datetime.now() + timedelta(days=1),
            login_id=login.id,
        )
        browser.close()
        logger.info("Login realizado")
        return session
