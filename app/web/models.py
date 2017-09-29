import math

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


class Paginator:
    def __init__(self, num_items, num_items_per_page, max_pages_per_block):
        self.num_items = num_items
        self.num_items_per_page = num_items_per_page
        self.max_pages_per_block = max_pages_per_block

    def make_paginator(self, active_page):
        pages_to_display = int(math.ceil(float(self.num_items)/float(self.num_items_per_page)))
        if pages_to_display <= self.max_pages_per_block:
            return [Page(page=page, active_page=active_page, label=page) for page in range(1, pages_to_display+1)]
        else:
            num_of_blocks = int(math.ceil(float(pages_to_display)/float(self.max_pages_per_block)))
            block_active_page = int(math.ceil(float(active_page)/float(self.max_pages_per_block)))
            if block_active_page == 1:
                pages = [Page(page=page, active_page=active_page, label=page) for page in range(1, self.max_pages_per_block+1)]
                pages.append(Page(page=self.max_pages_per_block+1, active_page=active_page, label=str(self.max_pages_per_block+1)+'-'+
                    str(self.max_pages_per_block*2)))
                return pages
            elif block_active_page == num_of_blocks:
                pages = [Page(page=page, active_page=active_page, label=page) for page in range((block_active_page-1)*self.max_pages_per_block+1, 
                    (block_active_page)*self.max_pages_per_block+1)]
                pages.insert(0, Page(page=self.max_pages_per_block*(block_active_page-1), active_page=active_page, label=str((block_active_page-2)*
                    self.max_pages_per_block+1)+'-'+str((block_active_page-1)*self.max_pages_per_block)))
                return pages
            else:
                pages = [Page(page=page, active_page=active_page, label=page) for page in range((block_active_page-1)*self.max_pages_per_block+1, 
                    pages_to_display)]
                pages.append(Page(page=self.max_pages_per_block*block_active_page+1, active_page=active_page, label=str(self.max_pages_per_block*block_active_page+1)+'-'+
                    str(self.max_pages_per_block*block_active_page+self.max_pages_per_block)))
                pages.insert(0, Page(page=self.max_pages_per_block*(block_active_page-1), active_page=active_page, label=str((block_active_page-2)*
                    self.max_pages_per_block+1)+'-'+str((block_active_page-1)*self.max_pages_per_block)))
                return pages



def make_paginator(pages_range, active_page):
    pages = [Page(page=page, active_page=active_page, label=page) for page in pages_range]
    return pages

