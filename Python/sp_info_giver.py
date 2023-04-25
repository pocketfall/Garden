import requests
from docxtpl import DocxTemplate
import tkinter as tk

class SpeciesFind(tk.Tk):
    def __init__(self):
        super().__init__()

        #setting up the window
        self.title('Info giver')
        self.geometry('1000x360')
        self.configure(bg= 'black')

        #setting up our attributes
        self.docx = DocxTemplate('info_tpl.docx')#None
        self.font = ('Comic Sans MS', 20, 'bold')
        self.frame_bg = ['aquamarine', 'lightpink']
        self.search_name_var = tk.StringVar()
        self.urls = [
            'https://api.obis.org/v3/occurrence?scientificname=marker1%20marker2',
            'https://api.obis.org/v3/taxon/marker1%20marker2',
            'https://api.obis.org/v3/statistics/env?scientificname=marker1%20marker2'
        ]
        self.search_terms = 'country, rightsholder, date_year, scientificname, individualcount, dropped, basisofrecord, locality, decimallongitude, eventdate, coordinateuncertaintyinmeters, institutioncode, recordedby, flags, sss, sst, shoredistance, bathymetry, is_marine, is_brackish, is_terrestrial, is_freshwater, kingdom, phylum, subphylum, infraphylum, class, subclass, order, suborder, infraorder, superfamily, family, genus, species, depth'.split(', ')
        self.err_label = None
        self.done_label = None
        self.sci_name = None
        self.api_call = 0
        self.tax_info = None
        self.occ_info = None
        self.env_info = None

        #setting up
        self.set_up()

    def set_up(self):
        #creating frames for the labels
        self.top_frame = tk.Frame(self, bg= 'black', width= 1280, height= 300)
        self.top_frame.pack(side= tk.TOP)

        #create labels
        self.create_widgets()

        #calling the loop function
        self.mainloop()

    def create_widgets(self):
        #the title label
        title_label = tk.Label(self.top_frame, text= 'Enter a scientific name',
                               font= (self.font[0], 40, 'bold'), fg= self.frame_bg[1], bg= 'black')
        title_label.grid(row= 0, column= 0)

        #the entry widget
        search_name = tk.Entry(self.top_frame, textvariable= self.search_name_var, font= self.font,
                               bg= 'white')
        search_name.grid(row= 1, column= 0, pady= 20)

        #enter button
        sub_btn = tk.Button(self.top_frame, font= self.font, text= 'SEARCH',
                            background= self.frame_bg[0], activebackground= 'white',
                            command= self.search)
        sub_btn.grid(row= 2, column= 0, pady= 10)

    def search(self):
        sp_name = self.search_name_var.get()
        if len(sp_name.split(' ')) > 2 or len(sp_name.split(' ')) == 0 or len(sp_name) == 0:
            #giving an error label
            self.err_label = tk.Label(self.top_frame, text= 'No valid name (according to this app)', bg= 'black',
                                      font= self.font, fg= self.frame_bg[1])
            self.err_label.grid(row= 3)
        if len(sp_name.split(' ')) == 2:
            #checking if the err_label is still present
            if self.err_label:
                self.err_label.destroy()

            #modifying urls to do the api calls
            for search_url in self.urls:
                search_url = search_url.replace('marker1', sp_name.split(' ')[0]).replace('marker2', sp_name.split(' ')[1])
                json_res = requests.get(search_url)
                json_res = json_res.json()
                self.sort_info(json_res)

    def sort_info(self, json_res):
        #this method is a nightmare lol
        searched = []
        weird_abt = []
        enum_list = list(enumerate(list(json_res.items())))

        #this if checks if the length of the enumerated list is less than 3
        #because the occurrance and checklist calls only have a length of 2, we'll know
        #whether it's those or the statistics call
        if len(enum_list) < 3:
            results_enli = enum_list[1][1][1]
            total_records = enum_list[0][1][1]
            searched.append(f'total_records: {total_records}')
            for item in results_enli:
                item_keys = list(item.keys())
                item_keys_lower = [low_keys.lower() for low_keys in item_keys]
                for key in range(len(item_keys_lower)):
                    if item_keys_lower[key] in self.search_terms:
                        if item_keys_lower[key] == 'flags' and item[item_keys[key]] not in weird_abt:
                            weird_abt.append(item[item_keys[key]])
                        else:
                            searched.append(f'{item_keys_lower[key]}: {item[item_keys[key]]}')
            match self.api_call:
                case 0:
                    self.occ_info = searched
                    self.weird_about = weird_abt
                case 1:
                    self.tax_info = searched
        else:
            sst_list = enum_list[0][1][1]
            sss_list = enum_list[1][1][1]
            dep_list = enum_list[2][1][1]
            env_lists = [sst_list, sss_list, dep_list]
            no_zero_dep_list = []
            no_zero_sst_list = []
            no_zero_sss_list = []
            for j in env_lists:
                for i in range(len(j)):
                    if j[i]['records'] != 0:
                        if j == sst_list:
                            no_zero_sst_list.append(j[i])
                        if j == sss_list:
                            no_zero_sss_list.append(j[i])
                        if j == dep_list:
                            no_zero_dep_list.append(j[i])
                if len(no_zero_sst_list) == 0:
                    no_zero_sst_list = j
                if len(no_zero_sst_list) == 0:
                    no_zero_sss_list = j
                if len(no_zero_sst_list) == 0:
                    no_zero_dep_list = j
            self.env_info = [no_zero_sst_list, no_zero_sss_list, no_zero_dep_list]
        if self.api_call < 2:
            self.api_call += 1
        else:
            self.api_call = 0
            self.create_doc(self.occ_info, self.tax_info, self.env_info)

    def create_doc(self, occ_info, tax_info, env_info):
        sp_name = self.search_name_var.get()
        sp_name = sp_name.lower()
        sp_name = sp_name[0].upper() + sp_name[1:]
        about_sciname = []

        #resorting the occurrance info since i chose to find too many entries and regret the decision
        for i in occ_info:
            i_split = i.split(':')
            if i_split[0] == 'country' or i_split[0] == 'flags' or i_split[0] == 'year' or i_split[0] == 'decimallongitude'\
                or i_split[0] == 'rightsholder' or i_split[0] == 'shoredistance' or i_split[0] == 'sss' or\
                i_split[0] == 'sst' or i_split[0] == 'bathymetry':
                    if i_split[0] == 'flags':
                        about_sciname.append(i)
                        about_sciname.append('OCCURRANCE END')
                    else:
                        about_sciname.append(i)

        #formatting the data so it looks readable
        about_sciname = str(about_sciname).replace('OCCURRANCE END', '\n').replace('[', '').replace(']', '').replace(',', '\n').replace('\'', '')
        about_tax_info = str(tax_info[1:]).replace('[', '').replace(']', '').replace(',', '\n').replace('\'', '')
        about_env_info = str(env_info).replace('[', '').replace(']', '').replace(',', '').replace('{', '').replace('}', '\n').replace('\'', '')

        #making the dictionary to change the markers in the document to the data we collected
        to_render = {
            'sciname': sp_name,
            'about_sciname': f"There are occurrances of the species in these countries and coordinates\nThere are also flags stating what it may be missing\n\n{about_sciname}",
            'sp_tax': f'Here is the taxonomic information\n\n{about_tax_info}',
            'sp_stats': f'Here is its environment information (sss, sst, depth) excluding any that did not have registers\n{about_env_info}'
        }
        #modifying, saving and showing a done message
        self.docx.render(to_render)
        self.docx.save(f'{sp_name}_info.docx')
        self.show_done(sp_name)

    def show_done(self, name):
        if not self.done_label:
            self.done_label = tk.Label(self.top_frame, text= f'{name} has been searched in OBIS.org\nCheck the folder where the app and template are for the document\nIts name is "{name}_info.docx"',
                 font= self.font, fg= 'pink', bg= 'black')
            self.done_label.grid()
        else:
            self.done_label.destroy()


if __name__ == '__main__':
    SpeciesFind()