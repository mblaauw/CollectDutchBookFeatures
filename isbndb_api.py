__author__ = 'MICH'
import isbndb
from is
ACCESS_KEY = "GH4FYZYE"

ISBNdbClient( access_key=ACCESS_KEY )



    def teardown(self):
        pass

    def test_connection(self):
        catalog = BookCollection(self.client)
        result  = catalog.isbn('9789049802400', results='authors')


if __name__ == "__main__":

    from unittest import main
    main( )