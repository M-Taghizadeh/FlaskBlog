from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

class MultipleCheckBoxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()