import pytest
from playwright.sync_api import sync_playwright
import time

@pytest.fixture()
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


def test_step1_validation(page):
    #Проверка доступности кнопки "Рассчитать ипотеку"
    page.goto("https://www.tbank.ru/mortgage/")
    button = page.get_by_role("button", name="Рассчитать ипотеку").first
    page.screenshot(path=".\\Artefact\\step1.png")
    assert button.is_enabled()

def test_step2_validation(page):
    # Проверка поля "Tип программы"
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.screenshot(path=".\\Artefact\\step2_1.png")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.screenshot(path=".\\Artefact\\step2_2.png")
    used_property = page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True)
    assert used_property.is_visible()
    new_property = page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Новостройки<!--p--><!--p-->", exact=True)
    assert new_property.is_visible()
    family_property = page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Семейная ипотека<!--p--><!--p-->", exact=True)
    assert family_property.is_visible()

def test_step3_validation(page):
    #проверка поля "Цена недвижимости позитивные"
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("aA") is False
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("499 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    sum_err_msg = page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Сумма кредита должна быть от")
    page.screenshot(path=".\\Artefact\\step3.png")
    assert sum_err_msg.is_visible()

def test_step4_validation(page):
    #Проверка полей первоночальный взнос и срок кредита
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    first_pay_pesent = page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text("46%")
    assert first_pay_pesent.is_visible()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").click()
    # assert page.locator(
    #     "[data-test=\"independent-parent-iframe\"] iframe"
    # ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("Aa") is False
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("70 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    minus20 = page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Не меньше 20% от недвижимости")
    page.screenshot(path=".\\Artefact\\step4.png")
    assert minus20.is_visible()

def test_step5_validation(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill("#")
    page.screenshot(path=".\\Artefact\\step5.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Используйте только символы русского алфавита и дефис").first.is_visible()


def test_step6_validation(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill(
        "Иванов Петр Ивановиx")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Иванов Петр Иванович").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").fill("7 (989) 944-44")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").click()
    page.screenshot(path=".\\Artefact\\step6.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Укажите номер мобильного телефона").is_visible()

def test_step7_validation(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
       "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill(
        "Иванов Петр Ивановиx")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Иванов Петр Иванович").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").fill("7 (989) 944-44-57")
    page.screenshot(path=".\\Artefact\\step7_1.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Укажите дату рождения").is_visible()

    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").fill("32.12.1996")
    page.screenshot(path=".\\Artefact\\step7_2.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Укажите корректную дату рождения").is_visible()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").fill("15.12.1996")

def test_step8_validation(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
       "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill(
        "Иванов Петр Ивановиx")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Иванов Петр Иванович").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").fill("+7 (901) 342-70-07")
    page.screenshot(path=".\\Artefact\\step8.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("800 000 ₽").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("013 ₽").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("— 29,135 %").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("24 %").is_visible()

def test_step9_sms_confirmation(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill(
        "Иванов Петр Ивановиx")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Иванов Петр Иванович").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").fill("+7 (901) 342-70-07")
    time.sleep(5)
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role("textbox",
                                                                                               name="Дата рождения * __.__.____").press(
        "Enter")
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role("button",
                                                                                               name="Далее").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role(
        "textbox", name="Код из СМС").fill("0000")
    page.screenshot(path=".\\Artefact\\step9.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Неверный код").is_visible()




def test_step10_validation_table2(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill(
        "Иванов Петр Ивановиx")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Иванов Петр Иванович").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").fill("+7 (901) 342-70-07")
    time.sleep(5)
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role("textbox",
                                                                                               name="Дата рождения * __.__.____").press(
        "Enter")
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role("button",
                                                                                               name="Далее").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role(
        "textbox", name="Код из СМС").fill("0000")
    time.sleep(5)
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Фамилия, Имя, ОтчествоИванов Петр Иванович").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.locator("label").filter(
        has_text="Мобильный телефон+7 (987) 441-71-60").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.locator("label").filter(has_text="Дата рождения15.12.1990")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("<!--p--><!--p-->Проверьте корректность данных в подсвеченных полях").is_visible()

def test_step11_validation_table2(page):
    page.goto("https://www.tbank.ru/mortgage/")
    page.get_by_role("button", name="Рассчитать ипотеку").first.click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Tип программы Вторичное жилье").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_text(
        "Вторичное жилье<!--p--><!--p-->", exact=True).click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Цена недвижимости, ₽").fill("150 0000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Первый взнос, ₽ 46%").fill("700 000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Срок кредита").fill("30")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Фамилия, Имя, Отчество *").fill(
        "Иванов Петр Ивановиx")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Иванов Петр Иванович").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Номер телефона * ___) ___-__-").fill("+7 (989) 944-44-57")
    time.sleep(5)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата рождения * __.__.____").press("Enter")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Далее").click()
    page.locator("[data-test=\"independent-parent-iframe\"] iframe").content_frame.get_by_role(
        "textbox", name="Код из СМС").fill("0000")
    time.sleep(5)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Серия и номер паспорта *").click()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Серия и номер паспорта *").fill("a") is False
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Серия и номер паспорта *").fill("45 67 89998")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Укажите корректные серию и номер паспорта").is_visible()
    page.screenshot(path=".\\Artefact\\step11.png")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Серия и номер паспорта *").fill("45 67 899988")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата выдачи *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Дата выдачи *").fill("17.15.2012")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Место рождения *").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Место рождения *").fill("Г. Самара")

    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Место рождения *").fill("г. Самара")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="г. Самара").locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Адрес регистрации *").click()

    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Адрес регистрации *").fill(
        "Самарская обл, г. Самара, поселок Прибрежный, ул Парусная, д.20 , кв 13"
    )
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role(
        "option", name="г Самара, поселок Прибрежный, ул Парусная, д 20, кв"
    ).locator("span").click()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Ежемесячный доход, ₽ *").fill("25000")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Ежемесячный доход, ₽ *").fill("9999")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Доход должен быть от 10 000")

    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("radio", name="Женат/замужем").is_checked()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("radio", name="Холост/не замужем").is_checked()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("radio", name="Женат/замужем").check()
    page.screenshot(path=".\\Artefact\\step12.png")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role(
        "textbox", name="Фамилия, имя и отчество супруга/супруги *"
    ).is_visible()
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role(
        "textbox", name="Фамилия, имя и отчество супруга/супруги *"
    ).fill("Петрова Юлия Ивановна")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("option", name="Петрова Юлия Ивановна").locator("span").click(timeout=60000)
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("textbox", name="Телефон супруга/супруги * ___").fill("+7 (987) 781-71-60")
    page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_role("button", name="Далее").click()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Недвижимость1 500 000 ₽").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Сумма кредита800 000 ₽").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Первый взнос700 000 ₽").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Платеж16 013 ₽ / мес")
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Срок30 лет").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Срок30 лет").is_visible()
    assert page.locator(
        "[data-test=\"independent-parent-iframe\"] iframe"
    ).content_frame.get_by_text("Тип программы")

