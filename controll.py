
from asyncio.windows_events import NULL
from turtle import shape
import numpy as np
import pandas as pd
import openpyxl
import constants
import timeit
import flask


ELEMENT_ARRAY_BASE_LOCATION = "C:\\Users\\DamnjanMilić\\Documents\\job_review\\21_09\\niz_elemenata_"  # Config constant
meta_data_location = "C:\\Users\\DamnjanMilić\\Documents\\job_review\\15_09\\MetadataAgriCoV1.0 (2).xlsx"
student_file_location =  "C:\\Users\\DamnjanMilić\\Documents\\job_review\\22_08\\proba_2.xlsm"#"C:\\Users\\DamnjanMilić\\Documents\\job_review\\21_09\\AgriCo Calc Test Control.xlsm"
Referent_data_location = "C:\\Users\\DamnjanMilić\\Documents\\job_review\\15_09\\REFE_control.xlsx"
student_id = 'ljuba_alicic@gmail.com_br_predmet'
EXPO_FILE_LOCATION = "C:\\Users\\DamnjanMilić\\Documents\\job_review\\Agri_co\\Data_set\\Expo.xlsx"  # Config constant
#EXPO_FILE_LOCATION = "C:\\Users\\DamnjanMilić\\Documents\\job_review\\15_09\\EXPO_control.xlsx"
#############
#### NEW ####
#############

def extract_student_id(array):
    for i in range(len(array)):
        current_value = str(array[i])
        array[i] = current_value[5:12]


def calculate_expo_table_getrieb(branch_id, expo_branch_array,student_id):
    # branch_id = ID tipa 1000 or 2000 or 3000
    # expo_branch_array -> niz za dati brench koji treba da se promeni

    dividers = constants.DIVERS_LIST_1000
    #final_table =  table_maker_getrieb_report(expo_branch_array, branch_id, dividers[i])
    final_table = []
    for i in range(len(dividers)):
        final_5000_0_table = table_maker_getrieb_report(expo_branch_array, branch_id, dividers[i],student_id)
        final_5000_0_table = np.delete(final_5000_0_table, (0), axis=0)
        if i == 0:
            final_table = final_5000_0_table
            
        else:
            #print(final_table)
            #final_table = np.delete(final_table, (0), axis=0)
            final_table = np.concatenate((final_table, final_5000_0_table), axis=0)

    return (final_table)

def table_maker_getrieb_report(transposed, n, id_name, student_id=""):
    niz = pd.read_excel(r"" + constants.ELEMENT_ARRAY_BASE_LOCATION + id_name + ".xlsx", skiprows=0, engine='openpyxl')
    array_elements = np.array(niz)

    final_array = np.zeros(len(transposed[:, 0]))
    value_array = list(range(0, 140))

    for i in value_array:
        final_array = np.column_stack((final_array, transposed[:, i]))

    change_strings_to_zero(transposed[:, 26])
    transposed[0][26] = constants.ANIMAL_POPULATION_YEAR_ZERO_NAME

    final_array = np.column_stack((final_array, transposed[:, 26]))
    annual_profit = np.subtract(transposed[:, 107], transposed[:, 76], where=transposed[:, 107] != transposed[0][107])
    annual_profit[0] = constants.ANNUAL_PROFIT_NAME
    final_array = np.column_stack((final_array, annual_profit))

    for i in range(len(array_elements[:, 0])):
        final_array = np.column_stack((final_array, calculation(transposed, array_elements[i], n )))

    divider = []
    for i in range(len(transposed[:, 76])):
        divider.append('After forage distribution' if n[5] == '1' else 'Before forage distribution')
    final_array = np.column_stack((final_array, divider))

    branch = []
    for i in range(len(final_array)):
        branch.append(n)
    final_array = np.column_stack((final_array, branch))

    branch = []
    for i in range(len(final_array)):
        branch.append(id_name)
    final_array = np.column_stack((final_array, branch))

    if student_id != "":
        branch = []
        for i in range(len(final_array)):
            branch.append(student_id)
        final_array = np.column_stack((final_array, branch))

    return final_array
#############
#### NEW ####
#############
def change_filter(array, value, code):
    for i in range(len(array)):
        if code == 'silo':
            if (array[i] != 3) and (array[i] != 4):
                array[i] = value
        elif code == 'zone':
            if (array[i] != 1) and (array[i] != 2):
                array[i] = value
        else:
            if array[i] != 1:
                array[i] = value
    return array


def change_filter_silo(array, value):
    for i in range(len(array)):
        if (array[i] != 3) and (array[i] != 4):
            array[i] = value
    return array 

def change_filter_zone(array, value):
    for i in range(len(array)):
        if (array[i] != 1) and (array[i] != 2):
            array[i] = value
    return array 

def change_filter_production(array, value):
    for i in range(len(array)):
        if array[i] != 1:
            array[i] = value
    return array 

def add_new_column(matrix, student_id):
    new_column = []
    for i in range(len(matrix)):
        new_column.append(student_id + str(i))
    matrix = np.column_stack((matrix, new_column))  
    return(matrix)


def add_two_new_rows(matrix):
    column_1000 = matrix[1].copy()
    column_2000 = matrix[2].copy()

    column_1000[-4] = 'After forage distribution'
    column_2000[-4] = 'After forage distribution'
    column_1000[-3] = '1000_1'
    column_2000[-3] = '2000_1'

    matrix = np.insert(matrix, matrix.shape[0], column_1000, axis = 0)
    matrix = np.insert(matrix, matrix.shape[0], column_2000, axis = 0)

    return(matrix)
    
def write_data_into_file(FILE_LOCATION, final_table, name_of_sheet ):
    start = timeit.timeit()
    df = pd.read_excel(r"" + FILE_LOCATION, sheet_name= name_of_sheet, engine='openpyxl')
    reference = pd.DataFrame(final_table, columns=df.columns)
    reference.drop(index=reference.index[0], axis=0, inplace=True)
    df = pd.concat([df, reference], axis=0)
    with pd.ExcelWriter(FILE_LOCATION, mode="a", engine="openpyxl",if_sheet_exists = "overlay") as writer:
        df.to_excel( writer, sheet_name= name_of_sheet, index=False, header=True)
    end = timeit.timeit()
    #print(start)
    #print(end)

def change_strings_to_zero(array):
    for i in range(len(array)):
        if type(array[i]) == str:
            array[i] = 0
    return array

def change_specific_array_to_zero(array_1, array_2, list_of_columns):
    for i in range(len(list_of_columns)):
        change_strings_to_zero(array_1[:,list_of_columns[i]])
        change_strings_to_zero(array_2[:,list_of_columns[i]])

def transpose_array(data_frame, should_stack=False, stack_array=None):
    transposed = np.array(data_frame)  # Transformation into np array
    if should_stack:
        transposed = np.vstack([stack_array, transposed])
    transposed[pd.isna(transposed)] = 0  # Transform nan into zero
    transposed = np.transpose(transposed, axes=None)  # Transposing the table
    return transposed

def make_refe_bin(ref_matrix, expo_matrix, code, first_line_expo ):

    numerator = 247 # this value is fixed.

    # in this function we make referent row with 0 and 1.

    list_of_columns = [1,247,250,34,31] # theese columns have some string in the columns
    change_specific_array_to_zero(ref_matrix, expo_matrix, list_of_columns)

    # maybe this part make problem? because maybe i all walue from new columns transport to zero?
    # yes it is. BUT I SOLVE YOU. izvini MIlane...
    # my name is error, fucking error
    # I will back.

    number_of_student_data = len(ref_matrix) # we need to add new criteraria so, if the number of the students smaller then 5 we need to fill matrix by zeros.
    if len(ref_matrix) !=0:
        for j in range(len(ref_matrix[0])):
            ref_matrix[:,j] = change_strings_to_zero(ref_matrix[:,j]) 
        for j in range(len(expo_matrix[0])):
            expo_matrix[:,j] = change_strings_to_zero(expo_matrix[:,j]) 
        i = 7 # first 7 values need to be equal to zero.
    else:
        i = 7
    new_row_refe = np.zeros(7)

    while i < numerator:
        if len(ref_matrix) !=0:
            max_refe = np.percentile(ref_matrix[:,i],90) # This is rule from methieu 
            min_refe = np.percentile(ref_matrix[:,i],10) # we need to find is the expo_value between these two values so if it is refe_value = 0 
        else:
            max_refe = 0
            min_refe = 0
        expo_value_array = expo_matrix[:,i]
        expo_value = expo_value_array[0]
        
        value_to_add = [1]

        if number_of_student_data <= 4 or expo_value == 0 or (expo_value <= max_refe and expo_value >= min_refe):
            value_to_add = [0]

        new_row_refe = np.append(new_row_refe, value_to_add)
        i += 1
             
    new_row_refe = np.append(new_row_refe, [0,code,0,student_id])
    new_row_refe = np.transpose(new_row_refe)
    new_row_refe_matrix = np.vstack([first_line_expo, new_row_refe])

    return(new_row_refe,new_row_refe_matrix)

def change_value_of_filter(array, first_value, second_value, first_string, second_string, third_string):
    for i in range(len(array)):
        if array[i] == first_value:
            array[i] = first_string
        elif array[i] == second_value:
            array[i] = second_string
        else:
            array[i] = third_string
    return(array)

def change_value_of_filter_value(value, first_value, second_value, first_string, second_string, third_string):
    if value == first_string:
        value = first_value
    elif value == second_string:
        value = second_value
    else:
        value = third_string
    return(value)  

def calculation(matrix, array, code):

   
    for j in range(len(matrix[0])):
        change_strings_to_zero(matrix[:,j])
    
    br = len(matrix[:,0])

    new = []
    new.append(array[0])
    i = 1

    if code != '2000_0':

        while i <br:
            if (matrix[i][array[int(7)]])  + int(matrix[i][array[int(8)]] == 0):
                new.append(0)
                i = i +1 
            else:    
                new.append(100*((matrix[i][array[2]] + matrix[i][array[3]] + matrix[i][array[4]]+ matrix[i][array[5]] + matrix[i][array[9]]+ matrix[i][array[10]] + matrix[i][array[11]] - matrix[i][array[6]])/(matrix[i][array[7]]  + matrix[i][array[8]])))
                i = i + 1
        new = np.array(new)
        j = 1
        new_1 = []
        new_1.append(new[0])

        if array[1] != 'yes':
            while j < br:
                new_1.append(float(new[j])/100)
                j+= 1
        else:
            while j < br:
                new_1.append(float(new[j]))
                j+= 1

    else:

        while i <br: 
            new.append(100*((matrix[i][array[2]] + matrix[i][array[3]] + matrix[i][array[4]]+ matrix[i][array[5]] + matrix[i][array[9]]+ matrix[i][array[10]] + matrix[i][array[11]] - matrix[i][array[6]])))
            i = i + 1
        new = np.array(new)
        j = 1
        new_1 = []
        new_1.append(new[0])

        if array[1] != 'yes':
            while j < br:
                new_1.append(float(new[j])/100)
                j+= 1
        else:
            while j < br:
                new_1.append(float(new[j]))
                j+= 1
    return(new_1)

def table_maker(transponovana,n,s, student_id=""):

    df = pd.read_excel(r"" + constants.meta_data_location, sheet_name='branchesNr', skiprows=1, engine='openpyxl')
    branchesNO = np.array(df)

    array_code_1 = []
    array_code_2 = []
    array_code_3 = []
    array_code_4 = []
    array_code_0 = []

    for i in range(len(branchesNO[:,1])):
        if branchesNO[i][1] == 1: 
            array_code_1.append(branchesNO[i][0])
        elif branchesNO[i][1] == 2:
            array_code_2.append(branchesNO[i][0])
        elif branchesNO[i][1] == 3:
            array_code_3.append(branchesNO[i][0])
        elif branchesNO[i][1] == 4:
            array_code_4.append(branchesNO[i][0])
        elif branchesNO[i][1] == 5:
            array_code_1.append(branchesNO[i][0])
        else:
            array_code_0.append(branchesNO[i][0])
    array_code_1.append('1000_0')

    id_name = "302070000_control" # this is constant and we can delete this nastavak.

    niz = pd.read_excel(r"" + ELEMENT_ARRAY_BASE_LOCATION + id_name + ".xlsx", skiprows=0, engine='openpyxl')
    array_elements = np.array(niz)
    

    divider = np.zeros(len(array_elements[:,0]))

    if np.isin(n, array_code_0):
        for i in range(len(divider)):
            divider[i] = int('0')
    elif np.isin(n, array_code_1):
        for i in range(len(divider)):
            divider[i] = int('41')
    elif np.isin(n, array_code_2):
        for i in range(len(divider)):
            divider[i] = int('12')   
    elif np.isin(n, array_code_3):
        for i in range(len(divider)):
            divider[i] = int('37')       
    elif np.isin(n, array_code_4):
        for i in range(len(divider)):
            divider[i] = int('26') 

    jedina_prava = np.zeros(len(transponovana[:,0]))
    divider = divider.astype(int)
    array_elements[:,8] = divider

    same_array =  list(range(0, 140))
    for i in same_array:
        jedina_prava = np.column_stack((jedina_prava, transponovana[:,i]))   

    change_strings_to_zero(transponovana[:,26])
    transponovana[0][26] = 'Tierbestand, Jahres-0, BeZ'

    jedina_prava = np.column_stack((jedina_prava,transponovana[:,26]))                              ###  Tierbestand, Jahres-0, BeZ     

    jahresgewinn = []
    jahresgewinn = np.subtract(transponovana[:,107] , transponovana[:,76], where = transponovana[:,107] != transponovana[0][107])
    jahresgewinn[0] = 'Jahresgewinn (ohne Vorsorge)'    ### Jahresgewinn (ohne Vorsorge)
    jedina_prava = np.column_stack((jedina_prava,jahresgewinn))     

    # ovde je okej

    # Automatisation

    for i in range(len(array_elements[:,0])):
        jedina_prava = np.column_stack((jedina_prava, calculation(transponovana ,array_elements [i], n)))

    # ovde nije okej

    # Chacker
    # add new to columns
    if n[5] == '1':
        diviator = []
        for i in range(len(transponovana[:,76])):
            diviator.append('After forage distribution')
        jedina_prava = np.column_stack((jedina_prava,diviator))    

        branch = []
        for i in range(len(jedina_prava)):
            branch.append(n[:-1] +'1')
        jedina_prava = np.column_stack((jedina_prava, branch))  
    else: 
        diviator = []
        for i in range(len(transponovana[:,76])):
            diviator.append('Before forage distribution')
        jedina_prava = np.column_stack((jedina_prava,diviator))    

        branch = []
        for i in range(len(jedina_prava)):
            branch.append(n[:-1] +'0')
        jedina_prava = np.column_stack((jedina_prava, branch))

    branch = []
    for i in range(len(jedina_prava)):
        branch.append(s)
    jedina_prava = np.column_stack((jedina_prava, branch))    

    branch = []
    for i in range(len(jedina_prava)):
        branch.append(student_id)
    jedina_prava = np.column_stack((jedina_prava, branch)) 

    return (jedina_prava)


def load_data(name_of_sheet, livestock_population_values, zone_code, produktions_code,ensilage_code): 
    # In this function we upload data from referent table
    # like in previous cases we need to delete some colums and rows
    # New in this function is that, that we need to filter data by 3 criteria:
    # zone_code, produktions_code, ensilage_code, this inforomation we get from the student file.
    # This function return matrix which  with filters which corespondes to the filters.

    df = pd.read_excel(r"" + constants.AGRICO_REFERENCE_FILE_LOCATION, sheet_name=name_of_sheet, skiprows=1, engine='openpyxl')
    df.drop(df.columns[[1, 2,3,4]], axis=1, inplace=True)       # Brise nepotrebne kolone 
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

    row_1 = list(df.columns.values)
    transposed = transpose_array(df, True, row_1)
    row_array = list(range(142, 153))
    transposed = np.delete(transposed, row_array, axis=1)

    first_row = transposed[0] # This is the first line with names of the columns, we need this row because later we will delete, because of caluclations.
    
    #print(name_of_sheet)
    #reference = pd.DataFrame(transposed)
    #reference.to_excel(excel_writer= r"C:\Users\DamnjanMilić\Documents\job_review\22_08\provera_transponovane_referentne.xlsx", index = False, header = False) 


    # In the next part we calculate referent row, for every branch (name_of_sheet). That means:
    # If in the student file we have several branches for exaple: 1000_0, 2000_0, 5000_1 we need export from this function only rows with this branch_s
    # so that certain colums match with fallowing filters.
    # Now I will list the filters from pbi, maybe i do something wrong in the python code, in generall. 
    # This work for this example but we need to check that:
    # codeZone = if('EXPO'[Zone cod.]=1, "Plain",if('EXPO'[Zone cod.]=2, "Hill","Mountain"))                    # from data we know that code zone can be some of this number: 1,2,3,4,5,6
    # CodeSilo = if('EXPO'[Silofütterung cod.]=3,"With",if('EXPO'[Silofütterung cod.]=4,"With","Without"))      # -||- : 0,1,2
    # CodeProduktForm = if('EXPO'[Produktionsform cod.]=1, "Bio","Conv")                                        # -||- : 0,1,2,3,4

    # now we will change that three column because we wont faster way to filter data

    ### Okej ajde nemoj dirati ovo, ov cu ujutru prepraviti otisla mi paznja ne znam gde sam. Radi ovo za ovaj primer.

    #print(transposed[:,3])
    # code_zone = change_value_of_filter(transposed[:,3], 1, 2, "Plain", "Hill", "Mountain")
    # code_silo = change_value_of_filter(transposed[:,5], 3, 4, "With", "With", "Without")
    # code_production = change_value_of_filter(transposed[:,4], 1, 1, "Bio", "Bio", "Conv")
    #print(code_zone) 
    # 
    #print(zone_code, produktions_code, ensilage_code)


    transposed[:,3] = change_filter(transposed[:,3], zone_code, 'zone') 
    transposed[:,4] = change_filter(transposed[:,4], produktions_code, 'production')
    transposed[:,5] = change_filter(transposed[:,5], ensilage_code, 'silo') 

    #print(len(transposed))   

    #reference = pd.DataFrame(transposed)
    #reference.to_excel(excel_writer= r"C:\Users\DamnjanMilić\Documents\job_review\22_08\transponovana_provera_11.xlsx", index = False, header = False) 
 

    if len(transposed) > 4 :

        ind = np.squeeze(np.asarray(transposed[:,3])) == zone_code
        transposed_2 = transposed[ind,:]
        ind_2 = np.squeeze(np.asarray(transposed_2[:,4])) == produktions_code
        transposed_3 = transposed_2[ind_2,:]
        ind_3 = np.squeeze(np.asarray(transposed_3[:,5])) == ensilage_code
        transposed = transposed_3[ind_3,:]
    #print(np.shape(transposed))
    else:
        transposed = transposed

    '''if produktions_code == 1:
        ind_2 = np.squeeze(np.asarray(transposed_2[:,4])) == produktions_code
        transposed_3 = transposed_2[ind_2,:]
    else:
        if np.shape(transposed_2) != (0, 1, 164):
            ind_2_2 = np.squeeze(np.asarray(transposed_2[:,4])) == 2
            ind_2_0 = np.squeeze(np.asarray(transposed_2[:,4])) == 0
            ind_2 = ind_2_2 +  ind_2_0
            transposed_3 = transposed_2[ind_2,:]
        else:
            transposed_3 = transposed_2

    if len(transposed_3) == 1:
        transposed =  transposed_3[0]
    else:  
        ind_3 = np.squeeze(np.asarray(transposed_3[:,5])) == 1
        ind_4 = np.squeeze(np.asarray(transposed_3[:,5])) == 2
        ind_5 = ind_3 + ind_4
        transposed = transposed_3[ind_5,:]'''
    #transposed = np.vstack([first_row, transposed]) 

    #reference = pd.DataFrame(transposed)
    #reference.to_excel(excel_writer= r"C:\Users\DamnjanMilić\Documents\job_review\22_08\transponovana_provera_11.xlsx", index = False, header = False) 


    branch = []
    for i in range(len(transposed)):
        branch.append(0)
    transposed = np.column_stack((transposed, branch))    

    curent_values = transposed[:,26]
  
    if '5000_0' in name_of_sheet:
        livestock_population_values = curent_values
    elif '5000_1' in name_of_sheet:
        for i, value in enumerate(curent_values):
            if value == 0:
                curent_values[i] = 46.5
    #
    return transposed, livestock_population_values

def expo_refe_table_controll(student_file_location, Referent_data_location, student_id, EXPO_FILE_LOCATION ):

    # In this function we makee referent table and expo t able for the pbi controll report

    # constants in the def
    deletion_array = list(range(0, 11))   
    s_1 = '302070000'
    livestock_population_values = []
    #

    # first we need to get values from expo

    df = pd.read_excel(r"" + student_file_location, sheet_name='Expo', skiprows=1, engine='openpyxl', na_values=['NaN'])
    delete_array = [0, 1] + list(range(3, 11))

    df.drop(df.columns[delete_array], axis=1, inplace=True)  # Deletes the unused columns
    transposed = transpose_array(df, False, None)            # Student data was uploaded into code

    zone_code = transposed[1][14]
    produktions_code = transposed[1][15]                     # these three lines we need to filter referent table
    ensilage_code = transposed[1][16]

    branches = transposed[:,10]                              # This is all branches that existed into student file
    all_codes = branches                                     # This is all branches that existed into student file
    which_branch_we_use = transposed[:,1]                    # This is array with -1,1,0 into fields, 1 mean that student has this branch into his data

    temporary_table = np.delete(transposed, deletion_array, axis=1) # now we delete usefull columns
    deletion_array = list(range(142, 153))
    temporary_table = np.delete(temporary_table, deletion_array, axis=1) # now we delete usefull columns
    a = temporary_table

    # into next line we read referent matrix:
    ref_matrix_5000_0, livestock_population_values = load_data(branches[1], livestock_population_values, zone_code, produktions_code,ensilage_code )
    # now we make referent table (this means that we make tale with all columns which we will use in the precalculations) from matrix
    final_5000_0_table = table_maker(ref_matrix_5000_0, branches[1], s_1, student_id) # I check this table, this is good

    # Now we make expo table for pbi

    new_expo = np.array(a[0]) # here we get first line with names of columns
    new_expo = np.transpose(new_expo) 
    new_expo_5000_0 = np.vstack([new_expo, a[1]])
    # next line make final caluclatios for the one branch for the one student
    final_value_from_expo_5000_0 = table_maker(new_expo_5000_0, branches[1], s_1,student_id) 
    # first_line_expo this will be one line for the one branch for example, one for 1000_0 one for 2000_0 ect
    first_line_expo = final_value_from_expo_5000_0[0]

    # in the next two lines we delete first lines from both caluclate matrix or rows because first lines ar names of the columns
    ref_matrix = np.delete(final_5000_0_table, 0, 0)
    expo_matrix = np.delete(final_value_from_expo_5000_0, 0, 0)

    #now we caluclate refe tables for pbi report and save expo

    new_row_refe = np.zeros(7) # first 7 columns need to be zeros into the refe_controll table because this is rule.
    change_strings_to_zero(ref_matrix[:,16]) # Maybe i dont need theese two lines but into these theese columns i have same text
    change_strings_to_zero(expo_matrix[:,31])

    # In the next line we make 
    new_line, new_row_refe_matrix = make_refe_bin(ref_matrix, expo_matrix, branches[1],first_line_expo )

    #expo
    EXPO_new = np.vstack([new_expo, a[1]]) 
    finall_expo = table_maker(EXPO_new, branches[1], s_1, student_id) # this will bi finall expo table which we will use in the pbi report
    branch_code_in_report = []


    #############
    #### NEW ####
    #############

    new_expo_getrieb = calculate_expo_table_getrieb( branches[1], EXPO_new,student_id)
    #print(new_expo_getrieb)
    # now we make the array which consist codes from expo table 
    #new_expo_getrieb = np.vstack([ finall_expo[0],new_expo_getrieb])
    #reference = pd.DataFrame(new_expo_getrieb)
    #reference.to_excel(excel_writer= r"C:\Users\DamnjanMilić\Documents\job_review\Agri_co\Data_set\EXPO_getrieb_1000.xlsx", index = False, header = False) 

    #############
    #### NEW ####
    #############

    for i in range(len(which_branch_we_use)):
        if which_branch_we_use[i] == 1:
            branch_code_in_report.append(str(all_codes[i]))

    branches = [] # dont ask me i dont know
    branches = branch_code_in_report
    
    i = 1

    # Okay, now we need to for every branch (1000,2000...) which exists into branch_code_in_report need to make array of 1 and 0 
    # which represent whether the expo value for a given index is within the range of reference values

    while i < len(branches):
        k = np.argwhere(all_codes == branches[i]) # find indx of the row for this branch, in the student table, every row represent different branch
        k_1 = k[0][0]                             # from some reason argwhere return matrix instead of integer
        livestock_population_values = []          # we dont need this array 

        # In the next line we upload data from next branch, referent values
        # ref_matrix_5000_0 always is the new line for referent table, sooo we (you) can do same thing like in last case, just put everything into for i am little afraid in this moment because maybe I will lose everything - ocajan sam.

        ref_matrix_5000_0, livestock_population_values = load_data(branches[i], livestock_population_values, zone_code, produktions_code,ensilage_code)

        final_5000_0_table = table_maker(ref_matrix_5000_0, branches[i], s_1, student_id) # this work fine.

        new_expo = np.array(a[0]) # aggain first row, Damnjan why?
        new_expo = np.transpose(new_expo)
        new_expo_5000_0 = np.vstack([new_expo, a[k_1]])
        final_value_from_expo_5000_0 = table_maker(new_expo_5000_0, branches[i], s_1,student_id)  # this is also work fine.
        
        #############
        #### NEW ####
        #############

        ### Here we calculate neww table for getrieb report:
        new_expo_getrieb_new = calculate_expo_table_getrieb(branches[i], new_expo_5000_0,student_id)
        #final_getrieb_table =
        new_expo_getrieb = np.vstack([new_expo_getrieb, new_expo_getrieb_new])
        #reference = pd.DataFrame(new_expo_getrieb)
        #reference.to_excel(excel_writer= r"C:\Users\DamnjanMilić\Documents\job_review\Agri_co\Data_set\EXPO_getrieb_1000.xlsx", index = False, header = False) 

        #############
        #### NEW ####
        #############


        first_line_expo = final_value_from_expo_5000_0[0] # aggain first row, Damnjan why?
        ref_matrix = np.delete(final_5000_0_table, 0, 0)
        expo_matrix = np.delete(final_value_from_expo_5000_0, 0, 0) # delete again first row, we can alsointegrate this into make_refe_bin maybe that is best solution
        new_row_refe = np.zeros(7)

        change_strings_to_zero(ref_matrix[:,16])
        change_strings_to_zero(expo_matrix[:,31])

        # Now we make referent row for this branch and after that we stack that row on the previous referent matrx: new_row_refe_matrix
        # soo in this moment 19:01 i think that i found a mistake, mistake is in the meke_refe_bin function.
        
        new_line_new, new_row_refe_matrix_new= make_refe_bin(ref_matrix, expo_matrix, branches[i],first_line_expo )
        new_row_refe_matrix = np.vstack([new_row_refe_matrix, new_line_new])
        #new_row_refe_check_matrix = np.vstack([new_row_refe_check_matrix, new_row_refe_check])
        
        new_line_expo = np.vstack([new_expo, a[k_1]])
        finall_expo_2 = table_maker(new_line_expo, branches[i], s_1,student_id) 
        finall_expo_2 = np.delete(finall_expo_2, (0), axis=0) ### This line delete first line of second table
        finall_expo= np.vstack([finall_expo, finall_expo_2])
        i = i + 1
    
    #############
    #### NEW ####
    #############

    new_expo_getrieb = np.vstack([new_expo_getrieb[0],new_expo_getrieb])

    #############
    #### NEW ####
    #############    

    #reference = pd.DataFrame(new_expo_getrieb)
    #reference.to_excel(excel_writer= r"C:\Users\DamnjanMilić\Documents\job_review\Agri_co\Data_set\EXPO_getrieb_1000.xlsx", index = False, header = False) 

    #############
    #### NEW ####
    #############

    for i in range(len(finall_expo[:,-1])):
        finall_expo[i][0] = 10e6

    finall_expo_1 = add_two_new_rows(finall_expo)
    new_row_refe_matrix_1 = add_two_new_rows(new_row_refe_matrix)

    expo_to_pbi = add_new_column(finall_expo_1, student_id)
    refe_to_pbi = add_new_column(new_row_refe_matrix_1, student_id)

    #for i in range(len(new_expo_getrieb[:,1])):
    #    print(expo_to_pbi[i][1])

    i = 1
    while i < len(new_expo_getrieb[:,1]):
        new_expo_getrieb[i][1] = str(expo_to_pbi[2][1])
        i = i + 1

    extract_student_id(new_expo_getrieb[:,1])
    extract_student_id(expo_to_pbi[:,1])

    #print("begin")
    write_data_into_file(EXPO_FILE_LOCATION, new_expo_getrieb, "EXPO_Betrieb")
    #print("Betrieb")
    write_data_into_file(EXPO_FILE_LOCATION, expo_to_pbi, "EXPO_control")
    #print("EXPO_C")
    write_data_into_file(EXPO_FILE_LOCATION, refe_to_pbi, "REFE_control")
    #print("REFE_C")       

# now we can call the function (finally).
expo_refe_table_controll(student_file_location, Referent_data_location, student_id, EXPO_FILE_LOCATION )