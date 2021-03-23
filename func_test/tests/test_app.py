from func_test import app
from io import StringIO


class TestApp:

    def setup_method(self):

        app.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]

        app.directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

    def test_check_document_existance(self):
        assert app.check_document_existance('2207 876234') is True

    def test_get_doc_owner_name(self, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('10006'))
        assert app.get_doc_owner_name() == 'Аристарх Павлов'

    def test_get_all_doc_owners_names(self):
        assert app.get_all_doc_owners_names() == {'Василий Гупкин', 'Геннадий Покемонов', 'Аристарх Павлов'}

    def test_remove_doc_from_shelf(self):
        app.remove_doc_from_shelf('2207 876234')
        assert app.directories['1'] == ['11-2', '5455 028765']

    def test_add_new_shelf(self):
        assert app.add_new_shelf('4') == ('4', True)

    def test_append_doc_to_shelf(self):
        app.append_doc_to_shelf('10007', '2')
        assert app.directories['2'] == ['10006', '10007']

    def test_delete_doc(self, monkeypatch):
        # app.input = lambda _: '2207 876234'
        monkeypatch.setattr('sys.stdin', StringIO('2207 876234'))
        app.delete_doc()
        assert app.documents == [
                {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
                {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
            ]

    def test_get_doc_shelf(self, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('11-2'))
        assert app.get_doc_shelf() == '1'

    def test_get_doc_shelf(self, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('11-2\n2\n'))
        app.move_doc_to_shelf()
        assert app.directories == {
                '1': ['2207 876234', '5455 028765'],
                '2': ['10006', '11-2'],
                '3': []
            }

    def test_add_new_doc(self, monkeypatch):

        app.documents = []
        app.directories = {
            '3': []
        }

        monkeypatch.setattr('sys.stdin', StringIO('554\npassport\nЖеня\n3'))
        app.add_new_doc()
        assert app.documents == [{"type": "passport", "number": "554", "name": "Женя"}];
        assert app.directories['3'] == ['554'];
