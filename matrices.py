import numpy as np
import streamlit as st
import pandas as pd
import base64
from io import BytesIO


def generate_matrix(rows, columns):
    original_matrix = np.random.choice(np.arange(100, 1000), size=(rows,
        columns), replace=False)

    new_matrix = np.copy(original_matrix)

    for j in range(columns):
        np.random.shuffle(new_matrix[:,j])

    position_matrix = np.zeros((rows,columns))
    for i in range(rows):
        for j in range(columns):
            new_pos = np.where(new_matrix == original_matrix[i,j])

            position_matrix[i,j] = new_pos[0][0] + 1

    old = pd.DataFrame(data=original_matrix)
    new = pd.DataFrame(data=new_matrix)
    position= pd.DataFrame(data=position_matrix)
    return old, new, position

def to_excel(old, new, position):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    old.to_excel(writer, index=False,header=False, sheet_name='Matriz Original')
    new.to_excel(writer, index=False,header=False, sheet_name='Matriz Reordenada')
    position.to_excel(writer, index=False, header=False, sheet_name='Matriz Posiciones')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(old, new, position):
    val = to_excel(old, new, position)
    b64 = base64.b64encode(val).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="matrices.xlsx">Download excel file</a>'


columns = st.text_input('Columnas:') 
rows = st.text_input('Filas:')

if rows and columns:
    old, new, position = generate_matrix(int(rows), int(columns))
    st.markdown(get_table_download_link(old, new, position), unsafe_allow_html=True)
