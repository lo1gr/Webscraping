This file will explain the organization of linkedin_scrape, but also how to use the different parts.


connections = driver.find_elements_by_xpath("//*[contains(text(), 'Manage your network')]")[0]

filter = driver.find_elements_by_xpath("//*[contains(text(), 'Search with filters')]")
filter.click()


svg_nest = driver.find_element_by_xpath("//section[@class='artdeco-alert-body']/button[@class='artdeco-dismiss']")
svg_nest.click()

TODO:
# write try error statement that retries the function 3 times if error (bc sometimes we might have some checks and we want to bypass that bc cant do those checks using selenium)
# Need to create a vitual environment to share the imported packages!


# works until here, line by line using cmd + enter