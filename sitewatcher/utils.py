def shrink_and_scroll_down(driver):
    driver.set_window_size(800, 600)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
