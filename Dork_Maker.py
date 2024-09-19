import datetime
import platform
import subprocess
import sys
import threading
import time

from colorama import init, Fore, Style

init(autoreset=True)

# Define the ASCII art
ascii_art = """
     
        ┳┓    ┓   ┳┳┓  ┓     
        ┃┃┏┓┏┓┃┏  ┃┃┃┏┓┃┏┏┓┏┓
        ┻┛┗┛┛ ┛┗  ┛ ┗┗┻┛┗┗ ┛ 
                     




                                                                              
"""

stylized_text = """ 



"""

files_paths = []
number_of_threads = 1
max_lines_output = 200000
number_of_finished_threads = 0
progress = 0
dpm = 0
generated_dorks = 0
is_aborted = False
dateNow = datetime.datetime.now()
allowed_dorks_types = ['search_function', 'parameter_type', 'page_type', 'keyword_1', 'keyword_2', 'site']
threads = []
working_threads = 0
total_dorks_to_generate = 1
current_file_counter = 0
generated_dorks_in_current_file = 0
ordered_dork_types_chosen_by_user = []


def clear_terminal():
    # Determine the command based on the platform
    try:
        if platform.system() == "Windows":
            command = "cls"
        else:
            command = "clear"

        # Use subprocess to call the appropriate command
        subprocess.call(command, shell=True)
        if sys.platform.startswith("win"):
            # For Windows
            _ = sys.stdout.write("\033[H\033[2J")
        else:
            # For Linux and Mac
            _ = sys.stdout.write("\033c")
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(Fore.RED + Style.BRIGHT + "\n>Stopping ...\n")
        sys.stdout.write(Fore.RED + Style.BRIGHT + "Check files paths\n")
        is_aborted = True
        exit()


def loadingTask():
    try:
        global total_dorks_to_generate
        global number_of_finished_threads, progress, dpm
        global generated_dorks, is_aborted
        global dateNow, current_file_counter, working_threads, ordered_dork_types_chosen_by_user

        loading_counter = 0
        loading_symbols = ["|", "/", "-", "\\"]

        clear_terminal()

        while number_of_finished_threads != number_of_threads and not is_aborted:

            progress = ((generated_dorks / total_dorks_to_generate) * 100) // 1
            print(Fore.GREEN + ascii_art + "\n\n" + Fore.GREEN + stylized_text + "\n\n")
            print(f"{Fore.GREEN}    [{Fore.BLUE}{loading_symbols[loading_counter]}{Fore.GREEN}] Generating dorks")
            print(f"{Fore.GREEN}    Total dorks to generate : {Fore.BLUE + str(total_dorks_to_generate)}")
            print(f"{Fore.GREEN}    Progress : {Fore.BLUE + str(progress)} %")
            print(f"{Fore.GREEN}    Dorks per minute : {Fore.BLUE + str(dpm)}")
            print(f"{Fore.GREEN}    Generated dorks : {Fore.YELLOW + str(generated_dorks)}")
            print(f"{Fore.GREEN}    Working threads : {Fore.BLUE + str(working_threads)}")
            print(f"{Fore.GREEN}    Finished threads : {Fore.BLUE + str(number_of_finished_threads)}")
            print(f"{Fore.GREEN}    Generated files : {Fore.BLUE + str(current_file_counter + 1)}")
            print(f"{Fore.GREEN}    Ordered dork types : {Fore.BLUE + ''.join(ordered_dork_types_chosen_by_user)}")

            move_up = "\033[F" * 33
            print(move_up, end='\r')

            loading_counter += 1

            if loading_counter >= len(loading_symbols):
                loading_counter = 0
            time.sleep(0.5)
        else:
            clear_terminal()
            progress = ((generated_dorks / total_dorks_to_generate) * 100) // 1
            print(Fore.GREEN + ascii_art + "\n\n" + Fore.GREEN + stylized_text + "\n\n")
            print(f"{Fore.GREEN}    Finished dorks")
            print(f"{Fore.GREEN}    Total dorks to generate : {Fore.BLUE + str(total_dorks_to_generate)}")
            print(f"{Fore.GREEN}    Progress : {Fore.BLUE + str(progress)} %")
            print(f"{Fore.GREEN}    Dorks per minute : {Fore.BLUE + str(dpm)}")
            print(f"{Fore.GREEN}    Generated dorks : {Fore.YELLOW + str(generated_dorks)}")
            print(f"{Fore.GREEN}    Working threads : {Fore.BLUE + str(working_threads)}")
            print(f"{Fore.GREEN}    Finished threads : {Fore.BLUE + str(number_of_finished_threads)}")
            print(f"{Fore.GREEN}    Generated files : {Fore.BLUE + str(current_file_counter + 1)}")
            print(f"{Fore.GREEN}    Ordered dork types : {Fore.BLUE + ''.join(ordered_dork_types_chosen_by_user)}")
            print(f"{Fore.GREEN}    Closing ... ")
        is_aborted = True
    except:
        sys.stdout.write(Fore.RED + Style.BRIGHT + "\n>Stopping ...\n")
        sys.stdout.write(Fore.RED + Style.BRIGHT + "Check files paths\n")
        is_aborted = True
        exit()


def dpmCalc():
    try:
        global number_of_threads
        global number_of_finished_threads, dpm
        global generated_dorks, is_aborted
        global dateNow

        while number_of_finished_threads != number_of_threads and not is_aborted:
            current_generated_dorks = generated_dorks
            time.sleep(60)
            dpm = generated_dorks - current_generated_dorks

    except:
        sys.stdout.write(Fore.RED + Style.BRIGHT + "\n>Stopping ...\n")
        sys.stdout.write(Fore.RED + Style.BRIGHT + "Check files paths\n")
        is_aborted = True
        exit()


def dorkThreadManneger(starting_indexs, dorks_per_thread):
    global files_paths, generated_dorks, current_file_counter, max_lines_output, generated_dorks_in_current_file
    global working_threads, number_of_finished_threads, is_aborted
    try:
        counter = 0

        droks_files_base = []

        for dork_file_path in files_paths:
            with open(dork_file_path, 'r') as dork_file:
                droks_files_base.append(dork_file.read().split("\n"))
                dork_file.close()

        while counter < dorks_per_thread and not is_aborted:

            if starting_indexs[0] < len(droks_files_base[0]) and starting_indexs[1] < len(droks_files_base[1]) and \
                    starting_indexs[2] < len(droks_files_base[2]) and starting_indexs[3] < len(droks_files_base[3]) and \
                    starting_indexs[4] < len(droks_files_base[4]) and starting_indexs[5] < len(droks_files_base[5]):

                dork_line = (droks_files_base[0][starting_indexs[0]] + droks_files_base[1][starting_indexs[1]] +
                             droks_files_base[2][starting_indexs[2]] + droks_files_base[3][starting_indexs[3]] +
                             droks_files_base[4][starting_indexs[4]] + droks_files_base[5][
                                 starting_indexs[5]] # + "after:2020-01-01"
                             + "\n")

                with open(f"./result/Dorks_{current_file_counter}.txt", 'a') as generated_dork_file:
                    generated_dork_file.write(dork_line)

                starting_indexs[5] += 1
                generated_dorks += 1
                generated_dorks_in_current_file += 1

                if generated_dorks_in_current_file >= max_lines_output:
                    generated_dorks_in_current_file = 0
                    current_file_counter += 1

                if starting_indexs[5] >= len(droks_files_base[5]):
                    starting_indexs[5] = 0
                    starting_indexs[4] += 1

                    if starting_indexs[4] >= len(droks_files_base[4]):
                        starting_indexs[4] = 0
                        starting_indexs[3] += 1

                        if starting_indexs[3] >= len(droks_files_base[3]):
                            starting_indexs[3] = 0
                            starting_indexs[2] += 1

                            if starting_indexs[2] >= len(droks_files_base[2]):
                                starting_indexs[2] = 0
                                starting_indexs[1] += 1

                                if starting_indexs[1] >= len(droks_files_base[1]):
                                    starting_indexs[1] = 0
                                    starting_indexs[0] += 1

                                    if starting_indexs[0] >= len(droks_files_base[0]):
                                        break

            elif starting_indexs[0] < len(droks_files_base[0]):

                if starting_indexs[5] >= len(droks_files_base[5]):
                    starting_indexs[5] = 0
                    starting_indexs[4] += 1

                    if starting_indexs[4] >= len(droks_files_base[4]):
                        starting_indexs[4] = 0
                        starting_indexs[3] += 1

                        if starting_indexs[3] >= len(droks_files_base[3]):
                            starting_indexs[3] = 0
                            starting_indexs[2] += 1

                            if starting_indexs[2] >= len(droks_files_base[2]):
                                starting_indexs[2] = 0
                                starting_indexs[1] += 1

                                if starting_indexs[1] >= len(droks_files_base[1]):
                                    starting_indexs[1] = 0
                                    starting_indexs[0] += 1

                                    if starting_indexs[0] >= len(droks_files_base[0]):
                                        break
                else:
                    break
            counter += 1
        number_of_finished_threads += 1
        working_threads -= 1
    except Exception as e:
        sys.stdout.write(Fore.RED + Style.BRIGHT + f"\n>Error occured {e}\n")
        sys.stdout.write(Fore.RED + Style.BRIGHT + ">Stopping ...\n")
        sys.stdout.write(Fore.RED + Style.BRIGHT + "Check files paths\n")


def mainThread():
    try:

        global files_paths
        global number_of_threads
        global generated_dorks, is_aborted, working_threads
        global dateNow, allowed_dorks_types, total_dorks_to_generate, ordered_dork_types_chosen_by_user

        print(Fore.GREEN + ascii_art + "\n\n\n\n" + Fore.GREEN + stylized_text + "\n\n\n\n")

        print(Fore.GREEN + Style.BRIGHT + "> Enter the the  order you want to generate from the following\n")

        print(
            Fore.GREEN + Style.BRIGHT + "> Note you must write it correctly as it's provided, but in the order you want")

        print(
            Fore.GREEN + Style.BRIGHT + "> Example input : [search_function][keyword_1][page_type][parameter_type][keyword_2][site]")

        print(
            Fore.GREEN + Style.BRIGHT + "> Available dork types : [search_function][parameter_type][page_type][keyword_1][keyword_2][site]")

        ordered_dork_types_chosen_by_user = input(f"{Fore.GREEN + Style.BRIGHT}> ")

        ordered_dork_types = ordered_dork_types_chosen_by_user

        ordered_dork_types = ordered_dork_types.replace("]", '').split("[")
        ordered_dork_types.remove('')

        if len(ordered_dork_types) != 6:
            print(f"{Fore.RED}> Check your input, only 6 dorks type are allowed, error occurred ...")
            return

        for dork_type in ordered_dork_types:
            if dork_type not in allowed_dorks_types:
                print(f"{Fore.RED}> Check your input and use the syntax provided as it's, error occurred ...")
                return

        files_counter = 0

        for dork_type in ordered_dork_types:
            print(
                f"{Fore.GREEN}> Enter the  path for the {Style.BRIGHT + dork_type + Style.NORMAL} file, example : C:\\users\\{dork_type}.txt")
            files_paths.append(input(f"{Fore.GREEN}> "))
            try:
                with open(files_paths[files_counter], 'r') as dork_file:
                    total_dorks_to_generate *= len(dork_file.read().split("\n"))
                    dork_file.close()
                files_counter += 1
            except Exception as e:
                sys.stdout.write(Fore.RED + Style.BRIGHT + f"\n> Dork file doesn't exist\n {e}")
                is_aborted = True
                exit()

        print(Fore.GREEN + Style.BRIGHT + "> Enter the number of threads")
        try:
            number_of_threads = int(input(f"{Fore.GREEN}> "))
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}> Error occurred, enter a number{e}")

        dorks_per_thread = total_dorks_to_generate // number_of_threads

        if total_dorks_to_generate < number_of_threads:
            number_of_threads = total_dorks_to_generate

        generated_dorks_counter = 0

        number_of_threads += 1
        starting_indexs = [0, 0, 0, 0, 0, 0]
        loading_thread = threading.Thread(target=loadingTask)
        dork_p_m_thread = threading.Thread(target=dpmCalc)

        loading_thread.start()
        dork_p_m_thread.start()
        while generated_dorks_counter <= total_dorks_to_generate:

            dork_thread = threading.Thread(target=dorkThreadManneger, args=(starting_indexs, dorks_per_thread))

            dork_thread.start()
            working_threads += 1

            if working_threads >= number_of_threads:
                dork_thread.join()

            generated_dorks_counter += dorks_per_thread

            files_counter = 5
            index_counter = generated_dorks_counter

            while files_counter >= 0:
                try:
                    with open(files_paths[files_counter], 'r') as dork_file:
                        starting_indexs[files_counter] = index_counter % len(dork_file.read().split("\n"))
                        index_counter //= len(dork_file.read().split("\n"))
                        dork_file.close()
                    files_counter -= 1

                except Exception as e:
                    sys.stdout.write(Fore.RED + Style.BRIGHT + f"\n> Dork file doesn't exist\n {e}")
                    is_aborted = True
                    exit()


    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"> Error occurred {e}")
        print(Fore.RED + Style.BRIGHT + "> Stopping ...")
        print(Fore.RED + Style.BRIGHT + "> Check files paths")
        is_aborted = True
        exit()


mainThread()
