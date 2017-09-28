class Page:
    page = 1
    label = 1
    active_page = 1
    css_class = ''

    def __init__(self, page, active_page, label):
        self.page = page
        self.active_page = active_page
        self.label = label
        if active_page == page:
            self.css_class = 'active'
        else:
            self.css_class = ''

    def __repr__(self):
        return '<Pager: {}>'.format(self.page)

    def go_to_block(self, num_pages_to_display, block_to_display):
        self.num_pages_to_display = num_pages_to_display
        self.block_to_display = block_to_display
        if block_to_display == 1:
            return [(num_pages_to_display+1, block_to_display*num_pages_to_display)]
        else:
            return [((block_to_display-1)*num_pages_to_display+1, num_pages_to_display*block_to_display), (num_pages_to_display*block_to_display+1, num_pages_to_display*block_to_display+num_pages_to_display)]


def make_paginator(pages_range, active_page, num_pages_to_display=None, block_to_display=None):
    if num_pages_to_display and block_to_display and num_pages_to_display > len(pages_range):
        page = Page(page=page, active_page=active_page)
        borders = page.go_to_block(num_pages_to_display, block_to_display)
        if len(borders) == 1:
            pages = [Page(page=page, active_page=active_page, label=page) for page in range(1, num_pages_to_display)]
            pages.append(Page(page=num_pages_to_display+1, active_page=active_page, label=borders[0](0)+'-'+borders[0](1)))
        else:
            pages = [Page(page=page, active_page=active_page, label=page) for page in range((block_to_display-1)*num_pages_to_display+1, num_pages_to_display*block_to_display)]
            pages.insert(Page(page=(block_to_display-1)*num_pages_to_display, active_page=active_page, label=borders[0](0)+'-'+borders[0](1)), 0)
            pages.append(Page(page=borders[1](0), active_page=active_page, label=borders[1](0)+'-'+borders[1](1)))
    else:
        pages = [Page(page=page, active_page=active_page) for page in pages_range]
    return pages
