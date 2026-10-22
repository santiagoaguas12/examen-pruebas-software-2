import book
import pytest
import library
import main
import user
from unittest.mock import patch


# TEMA: Marcadores de pytest (prueba desactivada con comillas triples).
# pytest.ini ya registra los marcadores unit y wip.
# Ejecutar solo las pruebas unit: pytest -m unit
# @pytest.mark.unit identifica esta prueba como unitaria.
# Comprueba que borrow() cambia el estado del libro a prestado.
"""
@pytest.mark.unit
def test_borrow_book():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    assert book1.title == "Orgullo y prejuicio"

    book1.borrow()
    assert book1.borrowed
"""





# TEMA: Marcadores de pytest (prueba desactivada con comillas triples).
"""
# Prueba el camino normal: prestar y después devolver el libro.
# Los assert verifican el estado antes y después de return_book().
@pytest.mark.unit
def test_return_book():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    assert book1.title == "Orgullo y prejuicio"

    book1.borrow()
    assert book1.borrowed
    book1.return_book()
    assert book1.borrowed == False
"""


# TEMA: pytest.raises().
# pytest.raises comprueba que la segunda llamada produce ValueError.
# La línea clave es with pytest.raises(ValueError, match=...).
@pytest.mark.unit
def test_borrow_two_times_book():
    book1 = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()









# TEMA: Fixtures con @pytest.fixture.
# Fixture = prepara una biblioteca nueva para cada prueba que la solicite.
# La usan test_library_init y test_library_user_registered.
@pytest.fixture
def lib_init():
    lib = library.Library()
    book_tenoch = book.Book("Orgullo y prejuicio", "Tenoch M", 2026, "ISBN0001")
    lib.add_book(book_tenoch)
    Tenoch = user.User("Tenoch", "0001")
    lib.add_user(Tenoch)

    return lib
# TEMA: Fixtures; usa lib_init.
# Fixture: comprueba que el libro preparado se puede prestar.
@pytest.mark.unit
def test_library_init(lib_init):
    lib = lib_init
    lib.borrow_book("0001", "ISBN0001")
    assert lib.books[0].borrowed == True

# TEMA: Fixtures; usa lib_init por segunda vez.
# Comprueba que la fixture también prepara un usuario.
@pytest.mark.unit
def test_library_user_registered(lib_init):
    assert lib_init.users[0].user_id == "0001"







# TEMA: monkeypatch.setattr().
# monkeypatch.setattr sustituye temporalmente un atributo real del libro.
# return_book() usa ese valor y deja el libro sin prestar.
@pytest.mark.unit
def test_setattr_book_borrowed(monkeypatch):
    book1 = book.Book("1984", "George Orwell", 1949, "ISBN001")
    monkeypatch.setattr(book1, "borrowed", True)
    book1.return_book()
    assert book1.borrowed == False


# TEMA: monkeypatch.delattr().
# monkeypatch.delattr elimina temporalmente un atributo del objeto.
# borrow() necesita borrowed y falla cuando el atributo no existe.
@pytest.mark.unit
def test_delattr_book_borrowed(monkeypatch):
    book1 = book.Book("1984", "George Orwell", 1949, "ISBN001")
    monkeypatch.delattr(book1, "borrowed")
    with pytest.raises(AttributeError, match="borrowed"):
        book1.borrow()


# TEMA: monkeypatch.setitem().
# monkeypatch.setitem cambia una entrada del diccionario settings.
# Sin usuarios ni libros, solo la rama desactivada puede terminar sin error.
@pytest.mark.unit
def test_loans_disabled(monkeypatch):
    lib = library.Library()
    monkeypatch.setitem(library.settings, "loans_enabled", False)
    assert lib.borrow_book("0001", "ISBN0001") is None


# TEMA: capsys.
# capsys captura lo que main.run() imprime con print().
# patch proporciona "0" para salir; la línea de estudio es readouterr().
@pytest.mark.wip
@pytest.mark.unit
def test_menu_capsys(capsys):
    with patch("builtins.input", return_value="0"):
        main.run()
    captured = capsys.readouterr()
    assert "--- Library System ---" in captured.out


# TEMA: Cobertura de caja blanca.
# Ejecuta la rama de Library.borrow_book() que intercambia ID e ISBN.
# Comando de cobertura: pytest --cov=library --cov-report=term-missing
@pytest.mark.unit
def test_library_swapped_ids_branch():
    lib = library.Library()
    lib.add_book(book.Book("1984", "George Orwell", 1949, "ISBN001"))
    lib.add_user(user.User("Ana", "001"))
    lib.borrow_book("ISBN001", "001")
    assert lib.books[0].borrowed == True


# TEMA: @pytest.mark.parametrize.
# PARAMETRIZE: ejecuta la misma prueba con tres títulos distintos.
# Se verifica el texto real que register_borrow guarda en el historial.
@pytest.mark.unit
@pytest.mark.parametrize(
    "title, expected",
    [
        ("1984", "Borrwed: 1984"),
        ("Moby Dick", "Borrwed: Moby Dick"),
        ("Dune", "Borrwed: Dune"),
    ],
)
def test_register_borrow_parametrized(title, expected):
    reader = user.User("Ana", "001")
    reader.register_borrow(book.Book(title, "Autor", 2026, "ISBN001"))
    assert reader.get_history() == [expected]

