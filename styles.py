"""
    This is my own code that I use in various data science projects:
    https://github.com/jaycode/inflation_damodaran/blob/main/styles.py
"""
import numpy as np

def format_row_wise(styler, formatter):
    """ Format rows """
    for row, row_formatter in formatter.items():
        row_num = styler.index.get_loc(row)

        for col_num in range(len(styler.columns)):
            styler._display_funcs[(row_num, col_num)] = row_formatter
    return styler

def style(df, t, key='row'):
    """ Style a DataFrame object with a template dict

    key is either 'row' or 'col'

    There are four types of Template dict values:
    ```
        {
            'rowname1': "Name of Row 1",
            'rowname2': lambda x: formatting_function(x)
            'rowname3': ("Name of Row 3", lambda x: formatting_function(x)),
            ('rowname4', 'colname1'): lambda x: formatting_function(x),
        }
    ```

    The fourth one is used to format a cell. Ordering is not important, so you can
    change a column name and then format a cell like so:
    ```
        {
            'rowname1': "New name",
            ('rowname1', 'colname1'): lambda x: formatting_function(x)

           # or, if `key` is 'col':
            'colname1': "New name",
            ('colname1', 'rowname1'): lambda x: formatting_function(x)
        }
    ```
    """
    def is_sequence(arg):
        return (not hasattr(arg, "strip") and
                hasattr(arg, "__getitem__") or
                hasattr(arg, "__iter__"))

    # format
    f = {}
    # rename
    r = {}
    for k in t:
        if type(t[k]) == str:
            r[k] = t[k]
        elif is_sequence(t[k]):
            r[k] = t[k][0]
            f[t[k][0]] = t[k][1]
        elif callable(t[k]):
            f[k] = t[k]

    # renamed df

    if key == 'row':
        rdf = df.rename(r)
        # styled df
        sdf = format_row_wise(rdf.style, f)
    elif key == 'col':
        rdf = df.rename(columns=r)
        sdf = rdf.style.format(f)
    else:
        raise(ValueError, "key must be either 'row' or 'col'")
    return sdf

# Formatter

def percent_or_null(x):
    """ Display as a percentage or NULL """
    if x is None or np.isnan(x):
        return "None"
    else:
        return f"{x:.2%}"

def round_or_null(x, n=2):
    """ Display as a round number or NULL """
    if x is None or np.isnan(x):
        return "None"
    else:
        return f"{x:,.{n}f}"

if __name__ == "__main__":
    # Copy the code below to a Jupyter notebook to display
    from IPython.display import display
    import pandas as pd

    test_df = pd.DataFrame(columns=('name', '2020', '2021'))
    test_df.set_index('name', inplace=True)
    test_df.loc['rev', :] = (100.212313, 70.709275)
    test_df.loc['roc', :] = (0.0455, 0.0189)

    tpl = {
        'rev': ("Revenue", lambda x: f"{round_or_null(x)}"),
        'roc': lambda x: f"{percent_or_null(x)}",
    }
    display(style(test_df, tpl))

    test_df = pd.DataFrame(columns=('year', 'rev', 'roc'))
    test_df.set_index('year', inplace=True)
    test_df.loc[2020, :] = (100.212313, 0.0455)
    test_df.loc[2021, :] = (70.709275, 0.0189)
    display(style(test_df, tpl, key='col'))

    # It is also possible to chain:
    def highlight(data, color='yellow'):
        '''
        highlight the maximum in a Series or DataFrame
        '''
        attr = 'background-color: {}'.format(color)
        return [attr]

    display(style(test_df, tpl, key='col').apply(highlight, subset=pd.IndexSlice[2021, 'roc']))
