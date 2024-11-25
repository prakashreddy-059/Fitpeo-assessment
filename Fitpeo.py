import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


driver = webdriver.Chrome()
driver.implicitly_wait(10)
url = 'https://www.fitpeo.com/'
driver.maximize_window()

#1. Navigate to the FitPeo Homepage
driver.get(url)

#2. Navigate to Revenue Calculator page
driver.find_element(By.LINK_TEXT, 'Revenue Calculator').click()
wait = WebDriverWait(driver, 10)
wait.until(ec.presence_of_element_located((By.XPATH, '//span[@class="MuiSlider-root MuiSlider-colorPrimary MuiSlider-sizeMedium css-16i48op"]')))

#3. Scroll Down to the Slider section
slider = driver.find_element(By.XPATH, '//span[@class="MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary css-1sfugkh"]')
driver.execute_script("arguments[0].scrollIntoView({ block: 'center', inline: 'nearest' });", slider)

#4. Adjust the slider
slider_width = slider.size['width']
slider_min = 0
slider_max = 100
target_percentage = 41
target_offset = (target_percentage / 100) * slider_width
action = ActionChains(driver)
action.click_and_hold(slider).move_by_offset(93.5, 0).release().perform()
time.sleep(2)
slider_position_1 = slider.get_attribute("style")

#5. Update the Text Field
input_field = driver.find_element(By.XPATH, "//input[@type='number']")
input_field.send_keys(Keys.CONTROL + "a")
input_field.send_keys(Keys.BACKSPACE)
input_field.send_keys('560')
time.sleep(2)
slider_position_2 = slider.get_attribute("style")

#6. Validate Slider Value
if slider_position_1 != slider_position_2:
    print("Validation Passed: Slider moved to reflect the updated text field value.")
else:
    print("Validation Failed: Slider position did not change.")

#7. Select CPT Codes
cpt_codes = ('CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474')
options = driver.find_elements(By.XPATH, "//div[@class='MuiBox-root css-1eynrej']")
time.sleep(1)
for option in options:
    heading = option.find_element(By.XPATH,".//p[@class='MuiTypography-root MuiTypography-body1 inter css-1s3unkt']").text.strip()
    if heading in cpt_codes:
        check_box = option.find_element(By.XPATH, ".//input[@type='checkbox']")
        check_box.click()
        time.sleep(1)

#8. Validate Total Recurring Reimbursement
TRR_expected = '$110700'
TRR_header = driver.find_element(By.XPATH, "//p[contains(text(), 'Total Recurring Reimbursement for all Patients Per Month:')]")
TRR_displayed = TRR_header.find_element(By.XPATH, ".//p").text.strip()
if TRR_expected == TRR_displayed:
    print("Validation Passed: The displayed value is correct.")
else:
    print(f"Validation Failed: Expected '{TRR_expected}', but found '{TRR_displayed}'.")

driver.quit()