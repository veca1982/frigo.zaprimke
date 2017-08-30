class Page:
    page = 1
    active_page = 1
    css_class = ''

    def __init__(self, page, active_page):
        self.page = page
        self.active_page = active_page
        if active_page == page:
            self.css_class = 'active'
        else:
            self.css_class = ''

    def __repr__(self):
        return '<Pager: {}>'.format(self.page)


def make_paginator(pages_range, active_page):
    pages = [Page(page=page, active_page=active_page) for page in pages_range]
    return pages
