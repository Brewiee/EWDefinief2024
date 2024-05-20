CLASSES TO IMPORT FOR CALLING THE EQUIVALENT CODE

MANAGMENT

from menu_management import MenuManagement
from order_management import OrderManagement
from table_management import TableManagementWidget
from Reservation_management import ReservationManagement

# from user_management import UserManagement-----------The user management should be outcommented on the Managment_choice_menu.py if the users management should not happen locally but based on different database


LIVE ORDERING 

On the other hand the live ordering system is just one call 

from ______gui_table import TableSelectionWindow


CUSTOMER RESERVATION

from Make_Reservations import CustomerWindow

for this you just call and execute the code and its opening and make reservation window 



LEVELS OF ACCESS

manager - access all
kassa - access OrderManagement / ReservationManagement / TableSelectionWindow
waiter - TableSelectionWindow



