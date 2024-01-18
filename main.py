# Include Libraries
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF



def find_index_data(data_name, n):
    index = 0
    for i in range((len(data_name))):

        counter = 0
        for k in range((len(data_name[i]))):
            if data_name[i][k] == '-':
                counter += 1

        if counter == n:
            index = i
            break

    return index

def input_data(data_file_name):

    data_name = np.loadtxt(data_file_name, delimiter=' ', dtype=str, usecols=(0))
    data_1 = np.loadtxt(data_file_name, delimiter=' ', dtype=str, usecols=(1))

    # vriskoume pou einai ta dedomena gia thn triti stili opou arxika einai null kai meta exoume mikos kai y
    index_zen_dist = find_index_data(data_name, 1)
    index_points = find_index_data(data_name, 0)

    data_2 = np.loadtxt(data_file_name, delimiter=' ', skiprows=index_zen_dist, dtype=str, usecols=(2))

    return index_zen_dist, index_points, data_name, data_1, data_2

def org_data(index_zen_dist, index_points, data_name, data_1, data_2, s_data, gon_z_data, gon_b_data, points_data, s_data_name, gon_z_data_name, gon_b_data_name, points_data_name, endiamesa_points_name):

    gon_b_index = 0
    gon_z_index = 0
    s_data_index = 0
    poits_data_index = 0
    data_2_index = 0

    for i in range(len(data_name)):

        if i < index_zen_dist:
            gon_b_data[gon_b_index, 0] = data_1[i]
            gon_b_data_name.append(data_name[i].split('-', 100))
            gon_b_index += 1

        if i >= index_zen_dist and i < index_points:
            gon_z_data[gon_z_index, 0] = data_1[i]
            gon_z_data_name.append(data_name[i].split('-', 100))
            gon_z_index += 1

            s_data[s_data_index, 0] = data_2[data_2_index]
            s_data_name.append(data_name[i].split('-', 100))
            endiamesa_points_name.append(data_name[i].split('-', 100)[1])
            s_data_index += 1
            data_2_index += 1

        if i >= index_points:
            points_data[poits_data_index, 0] = data_1[i]
            points_data[poits_data_index, 1] = data_2[data_2_index]
            points_data_name.append(data_name[i].split('-', 100))
            poits_data_index += 1
            data_2_index += 1

    #print(gon_b_data)
    #print(gon_b_data_name)
    #print(gon_z_data)
    #print(gon_z_data_name)
    #print(s_data)
    #print(s_data_name)
    #print(points_data)
    #print(points_data_name)

    return 0

def find_typos_odeusis(points_data_name, s_data_name):

    if len(points_data_name) == 4:
        typos = 'anoixti_pliros_e3art'
    else:
        if s_data_name[0][0] == s_data_name[len(s_data_name)-1][1]:
            typos = 'klisti_pliros_e3art'
        else:
            typos = 'anoixti_e3art'


    return typos

def check_a(a):

    while a < 0:
        a = a + 400

    while a > 400:
        a = a - 400

    return a
def check_a_tetartomorio(a, dx, dy):

    if dx >= 0 and dy >= 0:
        return a

    if dx <= 0 and dy >= 0:
        return a + 400

    if ( dx <= 0 and dy <= 0 ) or ( dx >= 0 and dy <= 0 ):
        return a + 200

def find_gon_a(p1, p2, points_data):

    dx = ( points_data[p2, 0] - points_data[p1, 0] )
    dy = ( points_data[p2, 1] - points_data[p1, 1] )

    a = np.arctan( dx / dy )*(200 / np.pi)
    a = check_a_tetartomorio(a, dx, dy)
    a = check_a(a)

    return a

def find_gon(b_name_1, b_name_2, b_name_3, gon_data, gon_data_name):

    b_gon = 0
    for k in range(len(gon_data)):
        if (gon_data_name[k][0] == b_name_1 or gon_data_name[k][0] == b_name_3) and gon_data_name[k][1] == b_name_2 and (gon_data_name[k][2] == b_name_3 or gon_data_name[k][2] == b_name_1):

            if gon_data_name[k][0] == b_name_3 and gon_data_name[k][2] == b_name_1:
                print('e3oteriki!')
                b_gon = 400 - gon_data[k, 0]
            else:
                b_gon = gon_data[k, 0]

    return b_gon
def find_a_themeliodes(a_1, gon_b_data, all_points_name, gon_b_data_name):

    a = a_1

    for i in range((len(gon_b_data))):
        p1 = all_points_name[i]
        p2 = all_points_name[i + 1]
        p3 = all_points_name[i + 2]

        a = a + find_gon(p1, p2, p3, gon_b_data, gon_b_data_name) + 200

    a = check_a(a)

    return a

def find_a_themeliodes_(gon_a, gon_b_data, a_2, a_1, cor, all_points_name, gon_b_data_name, index):

    # periptosi giaa anoixti me endiamesa simeia
    if index != 0:
        tmp = a_1
        tmpIndex = index
        backwards = 0
        p1 = gon_b_data_name[index][0]
        p2 = gon_b_data_name[index][1]
        p3 = gon_b_data_name[index][2]
        for i in range(len(gon_b_data)):

            gon_a[i, 0] = a_1 + find_gon(p1, p2, p3, gon_b_data, gon_b_data_name) + 200
            gon_a[i, 0] = check_a(gon_a[i, 0])
            a_1 = gon_a[i, 0]

            if p1 == gon_b_data_name[len(gon_b_data_name) - 1][0] and p2 == gon_b_data_name[len(gon_b_data_name) - 1][1] and p3 == gon_b_data_name[len(gon_b_data_name) - 1][2]:
                index = tmpIndex
                a_1 = check_a(tmp + 200)
                backwards = 1

            if backwards == 1:
                p3 = gon_b_data_name[index][0]
                p2 = gon_b_data_name[index][1]
                p1 = gon_b_data_name[index][2]
                index = index - 1
            else:
                p1 = gon_b_data_name[index][0]
                p2 = gon_b_data_name[index][1]
                p3 = gon_b_data_name[index][2]
                index += 1

            #print(p1,p2,p3, gon_a[i])
        return gon_a



    for i in range((len(gon_b_data) - 1 + cor)):
        p1 = all_points_name[i]
        p2 = all_points_name[i + 1]
        p3 = all_points_name[i + 2]

        gon_a[i, 0] = a_1 + find_gon(p1, p2, p3, gon_b_data, gon_b_data_name) + 200
        gon_a[i, 0] = check_a(gon_a[i, 0])
        a_1 = gon_a[i, 0]
    # na to fria3w, de leitourgei gia kathe dedomena logika dld an den einai stin seira
    if int(check_a(gon_a[len(gon_a) - 1, 0] + gon_b_data[len(gon_b_data) - 1, 0] + 200)) != int(a_2):
        if a_2 == 400 or a_2 == 0 or int(check_a(gon_a[len(gon_a) - 1, 0] + gon_b_data[len(gon_b_data) - 1, 0] + 200)) == 0 or int(check_a(gon_a[len(gon_a) - 1, 0] + gon_b_data[len(gon_b_data) - 1, 0] + 200)) == 400:
            print('isos provlimatika dedomena')
            return gon_a
        print('Provlima me gonia dieuthinisis')
        print('Ypologismeni apo themeliodes:', check_a(gon_a[len(gon_a) - 1, 0] + gon_b_data[len(gon_b_data) - 1, 0] + 200))
        print('Ypologismeni apo sintetagmenes:', a_2)
        exit(2)

    return gon_a

def diorthosi_b(gon_b_data, delta_b):

    for i in range((len(gon_b_data))):
        gon_b_data[i, 0] = gon_b_data[i, 0] + delta_b

    return gon_b_data

def find_gon_z(b_name_1, b_name_2, gon_z_data, gon_z_data_name):

    z_gon = 0
    for k in range(len(gon_z_data)):
        if (gon_z_data_name[k][0] == b_name_1 and gon_z_data_name[k][1] == b_name_2) or (gon_z_data_name[k][1] == b_name_1 and gon_z_data_name[k][0] == b_name_2):
            return gon_z_data[k, 0]

    if z_gon == 0:
        print('Den vrethike i gonia Z:', b_name_1, b_name_2)
        exit(2)

def calc_s(s_dist, s_data, gon_z_data, sum_dist, index, s_data_name, gon_z_data_name):

    if index != 0:
        tmpIndex = index
        backwards = 0
        p1 = s_data_name[index][0]
        p2 = s_data_name[index][1]
        for i in range(len(s_dist)):

            s_dist[i, 0] = find_s(p1, p2, s_data, s_data_name) * np.sin(find_gon_z(p1, p2, gon_z_data, gon_z_data_name) * np.pi / 200)
            sum_dist += s_dist[i, 0]

            if (p1 == s_data_name[len(s_data_name) - 1][0] and p2 == s_data_name[len(s_data_name) - 1][1]) or (p1 == s_data_name[len(s_data_name) - 1][1] and p2 == s_data_name[len(s_data_name) - 1][0]):
                index = tmpIndex
                backwards = 1

            if backwards == 1:
                p2 = s_data_name[index][0]
                p1 = s_data_name[index][1]
                index = index - 1
            else:
                p1 = s_data_name[index][0]
                p2 = s_data_name[index][1]
                index += 1

        return s_dist, sum_dist


    for i in range((len(s_dist))):

        s_dist[i, 0] = s_data[i, 0] * np.sin( gon_z_data[i, 0] * np.pi / 200 )
        sum_dist += s_dist[i, 0]

    return s_dist, sum_dist

def find_s(p1, p2, s_dist, s_data_name):

    temp_s = 0

    for k in range(len(s_data_name)):
        if (s_data_name[k][0] == p1 and s_data_name[k][1] == p2) or (s_data_name[k][0] == p2 and s_data_name[k][1] == p1):
            temp_s = s_dist[k, 0]
            break

    if temp_s == 0:
        print('Mikos den vrerhike apo dedomena:', p1, p2)
        exit(2)

    return temp_s
def calc_delta_X_Y(delta_X_Y, s_dist, gon_a, sum_X_Y, all_points_name, s_data_name, index):

    if index != 0:
        tmpIndex = index
        backwards = 0
        p1 = s_data_name[index][0]
        p2 = s_data_name[index][1]
        for i in range(len(delta_X_Y)):

            delta_X_Y[i, 0] = find_s(p1, p2, s_dist, s_data_name) * np.sin(gon_a[i, 0] * np.pi / 200)
            delta_X_Y[i, 1] = find_s(p1, p2, s_dist, s_data_name) * np.cos(gon_a[i, 0] * np.pi / 200)
            sum_X_Y[0, 0] += delta_X_Y[i, 0]
            sum_X_Y[0, 1] += delta_X_Y[i, 1]

            if p1 == s_data_name[len(s_data_name) - 1][0] and p2 == s_data_name[len(s_data_name) - 1][1]:
                index = tmpIndex
                backwards = 1

            if backwards == 1:
                p2 = s_data_name[index][0]
                p1 = s_data_name[index][1]
                index = index - 1
            else:
                p1 = s_data_name[index][0]
                p2 = s_data_name[index][1]
                index += 1


        return delta_X_Y



    for i in range((len(delta_X_Y))):
        p1 = all_points_name[i + 1] # to proto einai to trigometriko
        p2 = all_points_name[i + 2]

        delta_X_Y[i, 0] = find_s(p1, p2, s_dist, s_data_name) * np.sin( gon_a[i, 0] * np.pi / 200 )
        delta_X_Y[i, 1] = find_s(p1, p2, s_dist, s_data_name) * np.cos( gon_a[i, 0] * np.pi / 200 )
        sum_X_Y[0, 0] += delta_X_Y[i, 0]
        sum_X_Y[0, 1] += delta_X_Y[i, 1]

    return delta_X_Y

def calc_dx_dy(delta_dx_dy, omega_x, omega_y, sum_dist, s_dist, all_points_name, s_data_name, index):

    if index != 0:
        tmpIndex = index
        backwards = 0
        p1 = s_data_name[index][0]
        p2 = s_data_name[index][1]
        for i in range(len(delta_dx_dy)):

            delta_dx_dy[i, 0] = omega_x * (find_s(p1, p2, s_dist, s_data_name) / sum_dist)
            delta_dx_dy[i, 1] = omega_y * (find_s(p1, p2, s_dist, s_data_name) / sum_dist)

            if p1 == s_data_name[len(s_data_name) - 1][0] and p2 == s_data_name[len(s_data_name) - 1][1]:
                index = tmpIndex
                backwards = 1

            if backwards == 1:
                p2 = s_data_name[index][0]
                p1 = s_data_name[index][1]
                index = index - 1
            else:
                p1 = s_data_name[index][0]
                p2 = s_data_name[index][1]
                index += 1


        return delta_dx_dy


    for i in range((len(delta_dx_dy))):
        p1 = all_points_name[i + 1] # to proto einai to trigometriko
        p2 = all_points_name[i + 2]

        delta_dx_dy[i, 0] = omega_x * ( find_s(p1, p2, s_dist, s_data_name) / sum_dist )
        delta_dx_dy[i, 1] = omega_y * ( find_s(p1, p2, s_dist, s_data_name) / sum_dist )

    return delta_dx_dy

def calc_delta_X_Y_teliko(delta_X_Y_teliko, delta_dx_dy, delta_X_Y):

    for i in range((len(delta_X_Y_teliko))):
        delta_X_Y_teliko[i, 0] = delta_X_Y[i, 0] + delta_dx_dy[i, 0]
        delta_X_Y_teliko[i, 1] = delta_X_Y[i, 1] + delta_dx_dy[i, 1]

    return delta_X_Y_teliko

def cacl_x_y(x_y_data, delta_X_Y_teliko, points_data, j, index):

    if index != 0:
        tmpIndex = index
        backwards = 0
        x_arxiko = points_data[1, 0]
        y_arxiko = points_data[1, 1]
        for i in range(len(x_y_data)):

            x_y_data[i, 0] = x_arxiko + delta_X_Y_teliko[i, 0]
            x_y_data[i, 1] = y_arxiko + delta_X_Y_teliko[i, 1]
            x_arxiko = x_y_data[i, 0]
            y_arxiko = x_y_data[i, 1]

            if i == len(gon_b_data) - index - 1: # allazoume to arxiko simeio otan ftasoumes na exoume ypologizei kai to telteuo de3ia simeio
                index = tmpIndex
                backwards = 1
                x_arxiko = points_data[0, 0]
                y_arxiko = points_data[0, 1]


        return x_y_data


    x_arxiko = points_data[1, 0]
    y_arxiko = points_data[1, 1]

    for i in range((len(x_y_data))):
        x_y_data[i, 0] = x_arxiko + delta_X_Y_teliko[i, 0]
        x_y_data[i, 1] = y_arxiko + delta_X_Y_teliko[i, 1]
        x_arxiko = x_y_data[i, 0]
        y_arxiko = x_y_data[i, 1]


    x_check = x_y_data[len(x_y_data) - 1, 0] + delta_X_Y_teliko[len(delta_X_Y_teliko) - 1, 0]
    y_check = x_y_data[len(x_y_data) - 1, 1] + delta_X_Y_teliko[len(delta_X_Y_teliko) - 1, 1]


    if (int(x_check) != int(points_data[len(points_data) - j, 0]) or int(y_check) != int(points_data[len(points_data) - j, 1])) and j != 3:
        print('Provlima me ypologismes sintetatgmenes')
        print('Ypologismeno:', x_check)
        print('Apo dedomena:', points_data[len(points_data) - j, 0])
        exit(2)

    return x_y_data

def print_data(x_y_data, endiamesa_points_name, omega_s, gon_sfalma, points_data, points_data_name):

    print('Endiamesa Simeia: (x, y)')
    for i in range((len(x_y_data))):
        print(endiamesa_points_name[i], '(x, y):', round(x_y_data[i, 0], 3), ',', round(x_y_data[i, 1], 3))

    print('\nTrigometrika Simeia: (x, y)')
    for i in range(len(points_data)):
        print(points_data_name[i][0], '(x, y):', points_data[i, 0], ',', points_data[i, 1])


    print('\nGramiko Sfalma (mm):', round(omega_s*1000))
    print('Goniako Sfalma (cc):', round(abs(gon_sfalma*10000)))

    return 0

def orizontiografiki_epilisi(typos_odeusis, s_data, gon_b_data, s_data_name, gon_b_data_name, points_data, points_data_name, k, gon_z_data, x_y_data, endiamesa_points_name):

    a_1 = 0
    a_2 = 0
    delta_b = 0
    j = 0
    gon_sfalma = 0
    cor = 0
    index = 0

    if typos_odeusis == 'anoixti_pliros_e3art':
        # Ypologismos goniwn a apo sintetagmenes
        del endiamesa_points_name[-1] # diagrafi tou teleuteou onomato den xreiazete

        all_points_name.append(points_data_name[0][0])
        all_points_name.append(points_data_name[1][0])
        for i in range(len(endiamesa_points_name)):
            all_points_name.append(endiamesa_points_name[i])

        all_points_name.append(points_data_name[2][0])
        all_points_name.append(points_data_name[3][0])


        j = 2
        a_1 = find_gon_a(0, 1, points_data) # grad
        a_2 = find_gon_a(2, 3, points_data) # grad

        if points_data[0, 0] != points_data[len(points_data) - 2, 0]:
            k = k - 1

        else: # allios eoxume anoixti e3artimeni apo ta 2 idia simeia diladi to idio akro, xwris na einai kleisti odeusi
            k = k + 1
            a_2 = check_a(a_2)

        # Ypologismos deuteris a apo themeliodies
        a_2_ = find_a_themeliodes(a_1, gon_b_data, all_points_name, gon_b_data_name) # na balw na briskei an xreiazete na parei e3oteriki gonia

        if int(a_2_) == int(a_2) + 200:
            a_2 = a_2 + 200

        elif int(a_2_) + 200 == int(a_2):
            a_2_ = a_2 + 200

        gon_sfalma = a_2 - a_2_ # grad
        delta_b = gon_sfalma / (k + 1) # goaniako sfalma moirasmeno stis gonies, b arithmos goniwn

        # Print kapoia dedomena gia tin odeusi, ton typo kai ta simeia me tin seira pou ta ta xreisimopoiisi to programma
        print('Typos Odeusis:', typos_odeusis)
        print('Ta simeia me tin seira:')
        for i in range(len(all_points_name)):
            print(all_points_name[i], ' ', end='')
        print('\n')


    if typos_odeusis == 'klisti_pliros_e3art':

        del endiamesa_points_name[-1] # diagrafi tou teleuteou onomato den xreiazete

        all_points_name.append(points_data_name[0][0])
        all_points_name.append(points_data_name[1][0])
        for i in range(len(endiamesa_points_name)):
            all_points_name.append(endiamesa_points_name[i])

        all_points_name.append(points_data_name[1][0])
        all_points_name.append(endiamesa_points_name[0])

        if gon_b_data_name[0][1] != points_data_name[1][0]: # periptosi pou to simeio den einai to imisahero kai einai pio meta apla to bazoume proto
            all_points_name.clear()
            index = 0 #
            for i in range(len(gon_b_data)):
                if gon_b_data_name[i][1] == points_data_name[1][0]:
                    index = i

            all_points_name.append(points_data_name[0][0])
            all_points_name.append(points_data_name[1][0])

            index_s_data = 0
            for k in range(len(s_data_name)):
                if s_data_name[k][1] == gon_b_data_name[index][1]:
                    index_s_data = k

            for k in range(len(s_data_name)):
                all_points_name.append(s_data_name[index_s_data + 1][1])

                if index_s_data + 1 == len(s_data_name) - 1:
                    index_s_data = - 1
                else:
                    index_s_data += 1


        # to k menei idio giati to sxima klinei
        j = 1
        a_1 = find_gon_a(0, 1, points_data) # grad

        a_2 = a_1 + 200
        a_2 = check_a(a_2)

        a_2_ = find_a_themeliodes(a_1, gon_b_data, all_points_name, gon_b_data_name)

        gon_sfalma = a_2 - a_2_  # grad
        delta_b = gon_sfalma / (k + 1)  # goaniako sfalma moirasmeno stis gonies

        print('Typos Odeusis:', typos_odeusis)
        print('Ta simeia me tin seira:')
        for i in range(len(all_points_name)):
            print(all_points_name[i], ' ', end='')
        print('\n')


    if typos_odeusis == 'anoixti_e3art':

        k = k - 1
        j = 3
        a_1 = find_gon_a(0, 1, points_data) # grads
        cor = 1


        all_points_name.append(points_data_name[0][0])
        all_points_name.append(points_data_name[1][0])
        for i in range(len(endiamesa_points_name)):
            all_points_name.append(endiamesa_points_name[i])


        if all_points_name[0] != points_data_name[0][0]: # auto simenei oti exoume gnosta 2 endiamesa simeia kai oxi ta 2 arxika

            for i in range(len(gon_b_data_name)):
                if (gon_b_data_name[i][0] == points_data_name[0][0] or gon_b_data_name[i][1] == points_data_name[0][0]) and (gon_b_data_name[i][1] == points_data_name[1][0] or gon_b_data_name[i][0] == points_data_name[1][0]):
                    index = i

                    for k in range(len(s_data)):
                        if (s_data_name[i][0] == points_data_name[0][0] or s_data_name[i][0] == points_data_name[1][0]) and (s_data_name[i][1] == points_data_name[0][0] or s_data_name[i][1] == points_data_name[1][0]):
                            del s_data[k, 0]
                            del s_data_name[k]

                    all_points_name.clear()
                    for j in range(len(s_data_name)):
                        all_points_name.append(s_data_name[i][0])
                        all_points_name.append(s_data_name[i][1])


            if gon_b_data_name[len(gon_b_data_name) - 1][1] == points_data_name[len(points_data_name) - 2][0]: # tote exoume gnosta ta 2 teleutea seimeia
                print('test')

                all_points_name.clear()
                all_points_name.append(points_data_name[0][0])
                all_points_name.append(points_data_name[1][0])

                for i in range(len(endiamesa_points_name)):
                    all_points_name.append(endiamesa_points_name[i])

                a_1 = check_a(a_1 + 200)
                gon_b_data = np.flip(gon_b_data, 0)
                gon_b_data_name.reverse()

                s_data = np.flip(s_data)
                s_data_name.reverse()

                gon_z_data = np.flip(gon_z_data)
                gon_z_data_name.reverse()

        print('Typos Odeusis:', typos_odeusis)
        print('Ta simeia me tin seira:') # prepei na ftia3w ta onomata apo tin arxei (na ta pernw apo tis gonies b kalitera)
        for i in range(len(all_points_name)):
            print(all_points_name[i], ' ', end='')
        print('\n')
        print('endiamesa ', endiamesa_points_name)
        exit(2)



    # Epilusi Odeusis

    gon_b_data = diorthosi_b(gon_b_data, delta_b)

    gon_a = np.zeros((k, 1))
    gon_a = find_a_themeliodes_(gon_a, gon_b_data, a_2, a_1, cor, all_points_name, gon_b_data_name, index)


    s_dist = np.zeros((k, 1))
    sum_dist = 0
    s_dist, sum_dist = calc_s(s_dist, s_data, gon_z_data, sum_dist, index, s_data_name, gon_z_data_name)


    delta_X_Y = np.zeros((k , 2))
    sum_X_Y = np.zeros((1, 2))
    delta_X_Y = calc_delta_X_Y(delta_X_Y, s_dist, gon_a, sum_X_Y, all_points_name, s_data_name, index)


    x_2_ = points_data[1, 0] + sum_X_Y[0, 0]
    y_2_ = points_data[1, 1] + sum_X_Y[0, 1]

    if typos_odeusis != 'anoixti_e3art':
        if typos_odeusis == 'anoixti_pliros_e3art':
            omega_x = points_data[len(points_data) - 2, 0] - x_2_  # gramiko sfalma kata x
            omega_y = points_data[len(points_data) - 2, 1] - y_2_  # gramiko sfalma kata y
        else: # gia tin kleisti pliros e3artimeni
            omega_x = points_data[len(points_data) - 1, 0] - x_2_  # gramiko sfalma kata x
            omega_y = points_data[len(points_data) - 1, 1] - y_2_  # gramiko sfalma kata y
    else:
        omega_x = 0
        omega_y = 0

    omega_s = np.sqrt(omega_x ** 2 + omega_y ** 2)  # oliko gramiko sfalma


    delta_dx_dy = np.zeros((k, 2))
    delta_dx_dy = calc_dx_dy(delta_dx_dy, omega_x, omega_y, sum_dist, s_dist, all_points_name, s_data_name, index)


    delta_X_Y_teliko = np.zeros((k, 2))
    delta_X_Y_teliko = calc_delta_X_Y_teliko(delta_X_Y_teliko, delta_dx_dy, delta_X_Y)

    if typos_odeusis == 'anoixti_e3art':
        k = k + 1

    x_y_data = np.zeros((k - 1, 2))
    x_y_data = cacl_x_y(x_y_data, delta_X_Y_teliko, points_data, j, index)

    print_data(x_y_data, endiamesa_points_name, omega_s, gon_sfalma, points_data, points_data_name)


    return x_y_data

def find_k(typos_odeusis, k):

    if typos_odeusis == 'anoixti_pliros_e3art':
        return k - 2 # 2 stahera (trigonometrika simeia)

    else:
        return k - 1 # 1 stahera (trigonometrika simeia)

def mikoi_t0_egsa87(s_data, x_meso):

    for i in range(len(s_data)):
        s_data[i, 0] = s_data[i, 0] * ( 0.9996 + 0.012311 * ( (x_meso/10**6)  - 0.5)**2 )

    return s_data

def yhometriki_epilisi(gon_z_data, s_data, dh, Y_O, Y_S):
    kappa = 1 # sintelestis diathlasis, edw bazoume 1 gia na apalithi kathos oi metrisi einai metabasi-epistrofi, an den einai esti prepei na mpei mia timi tou
    for i in range((len(dh))):
        DH = s_data[i, 0] * np.cos( gon_z_data[i, 0] * np.pi / 200 ) + Y_O - Y_S- + ( (1 - kappa)*(s_data[i, 0]**2)*(np.sin( gon_z_data[i, 0] * np.pi / 200 )**2) )


    return dh

def plot_data(x_y_data, points_data, points_data_name, endiamesa_points_name, typos_odeusis):

    plt.figure(figsize=(11.69, 8.27)) # bazoume to sxedio na einai se megethos A4

    text_data = []

    if typos_odeusis == 'anoixti_pliros_e3art':
        x = np.zeros((len(x_y_data) + len(points_data), 1))
        y = np.zeros((len(x_y_data) + len(points_data), 1))

        x[0, 0] = points_data[0, 0]
        y[0, 0] = points_data[0, 1]
        x[1, 0] = points_data[1, 0]
        y[1, 0] = points_data[1, 1]
        text_data.append(points_data_name[0][0])
        text_data.append(points_data_name[1][0])

        offset_stahero = 2
        offset = offset_stahero
        for i in range(len(x_y_data)):
            x[i+offset_stahero, 0] = x_y_data[i, 0]
            y[i+offset_stahero, 0] = x_y_data[i, 1]
            text_data.append(endiamesa_points_name[i])
            offset += 1

        x[offset, 0] = points_data[2, 0]
        y[offset, 0] = points_data[2, 1]
        x[offset + 1, 0] = points_data[3, 0]
        y[offset + 1, 0] = points_data[3, 1]
        text_data.append(points_data_name[2][0])
        text_data.append(points_data_name[3][0])

        for i in range((len(text_data))):
            plt.text(x[i, 0], y[i, 0], text_data[i], fontdict=None, fontsize=13.5, position=(x[i, 0], y[i, 0] + 3.5))


    if typos_odeusis == 'klisti_pliros_e3art':
        x = np.zeros((len(x_y_data) + len(points_data) + 1, 1))
        y = np.zeros((len(x_y_data) + len(points_data) + 1, 1))

        x[0, 0] = points_data[0, 0]
        y[0, 0] = points_data[0, 1]
        x[1, 0] = points_data[1, 0]
        y[1, 0] = points_data[1, 1]
        text_data.append(points_data_name[0][0])
        text_data.append(points_data_name[1][0])

        offset_stahero = 2
        offset = offset_stahero
        for i in range(len(x_y_data)):
            x[i+offset_stahero, 0] = x_y_data[i, 0]
            y[i+offset_stahero, 0] = x_y_data[i, 1]
            text_data.append(endiamesa_points_name[i])
            offset += 1

        x[offset, 0] = points_data[1, 0]
        y[offset, 0] = points_data[1, 1]

        for i in range((len(text_data))):
            plt.text(x[i, 0], y[i, 0], text_data[i], fontdict=None, fontsize=13.5, position=(x[i, 0], y[i, 0] + 3.5))

    if typos_odeusis == 'anoixti_e3art':
        x = np.zeros((len(x_y_data) + len(points_data), 1))
        y = np.zeros((len(x_y_data) + len(points_data), 1))

        x[0, 0] = points_data[0, 0]
        y[0, 0] = points_data[0, 1]
        x[1, 0] = points_data[1, 0]
        y[1, 0] = points_data[1, 1]
        text_data.append(points_data_name[0][0])
        text_data.append(points_data_name[1][0])

        offset_stahero = 2
        offset = offset_stahero
        for i in range(len(x_y_data)):
            x[i+offset_stahero, 0] = x_y_data[i, 0]
            y[i+offset_stahero, 0] = x_y_data[i, 1]
            text_data.append(endiamesa_points_name[i])
            offset += 1


        for i in range((len(text_data))):
            plt.text(x[i, 0], y[i, 0], text_data[i], fontdict=None, fontsize=13.5, position=(x[i, 0], y[i, 0] + 3.5))


    plt.plot(x, y, '.b-', zorder=1)  # a blue color line
    plt.scatter(x, y, s=150, marker='.', color='red')

    plt.title('Sxedio Diktiou')  # Title of the figure
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.show()
    #if typos_odeusis == 'anoixti_e3art'


        #plt.text(x[i, 0], y[i, 0], points_data_name[i],fontdict=None, fontsize=13.5, position= (x[i, 0], y[i, 0]+3.5))

    #x[len(x_y_data), 0] = x_y_data[0, 0]
    #y[len(x_y_data), 0] = x_y_data[0, 1]

    #plt.figure(figsize=(11.69, 8.27))

    #plt.savefig("sxedio_diktiou.pdf", dpi=200)

    return 0

if __name__ == '__main__':

    #data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\anoixti_pliros_e3art.txt"
    #data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\klisti_e3art.txt"
    data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\anoixti_e3art.txt"
    #data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\real_data.txt"
    #data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\anoixti_e3art_TEST.txt"
    #data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\anoixti_e3art_test_me_endiamesa.txt"
    #data_file_name = "C:\\Users\\nikos\\OneDrive\\Files\\Projectakia\\Geodesy_Projects\\Dedomena\\\Odeusis\\anoixti_e3art_gnosta_2_teleutea.txt"

    # input raw data from txt file
    index_zen_dist, index_points, data_name, data_1, data_2 = input_data(data_file_name)

    # organize data from input
    s_data = np.zeros((index_points - index_zen_dist, 1))
    s_data_name = []
    gon_z_data = np.zeros((index_points - index_zen_dist, 1))
    gon_z_data_name = []
    gon_b_data = np.zeros((index_zen_dist, 1))
    gon_b_data_name = []
    points_data = np.zeros((len(data_name) - index_points, 2))
    points_data_name = []
    endiamesa_points_name = []
    all_points_name = []

    org_data(index_zen_dist, index_points, data_name, data_1, data_2, s_data, gon_z_data, gon_b_data, points_data, s_data_name, gon_z_data_name, gon_b_data_name, points_data_name, endiamesa_points_name)

    #mikoi_t0_egsa87(s_data, (points_data[0, 0] + points_data[1, 0])/2) #+ points_data[len(points_data) - 1, 0] / 2))

    # Epilisi odeusis
    typos_odeusis = find_typos_odeusis(points_data_name, s_data_name)

    k = find_k(typos_odeusis, len(np.unique(gon_b_data_name))) # arithmos korifwn xwris ta trigometrika (ginete esti giati mporei na exei metrithi mikos pros trigonometriko)

    x_y_data = np.zeros((k - 1, 2))
    x_y_data = orizontiografiki_epilisi(typos_odeusis, s_data, gon_b_data, s_data_name, gon_b_data_name, points_data, points_data_name, k, gon_z_data, x_y_data, endiamesa_points_name)


    # plot data
    plot_data(x_y_data, points_data, points_data_name, endiamesa_points_name, typos_odeusis)