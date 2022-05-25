import re
import os
import datetime

class TextTransformerType1:
    #2019/5/8 上午 11:30:34	0.454244	1.338773	0.599610	0.651245	0.944937	0.519692	0.533834	3.466636	3.102729	3.667746	2.939275	0.249186	1.352257	1.785888	1.388902	57.900000
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.reg = "^\d*/\d*/\d* 上*下*午 \d\d:\d\d:\d\d(\t\d*.\d*)*"    
        self.rbias = [9000,14900,21800,9900,14800,8100,9000,14900,32600,9000,5100,3300,46500,2200]
        self.input_file = None
        self.output_file = None
        self.first_time = None
        
    def entrance(self, file):
        self.input_file = file
        self.output_file =  self.output_folder +'\\'+ self.input_file.split('\\')[-1].replace('.txt', '.ndjson')
        print(self.input_file)
        print(self.output_file)
        self.find_first_time()
        if not self.check_file():
            self.make_fake_filemeta()
        self.make_fake_preset_meta()
        self.open_file()
    
    def open_file(self):
        with open(self.input_file, 'r') as f:
            content = f.readlines()
            for index, each_line in enumerate(content):
                if re.match:
                    if len(each_line.split('\t')) == 17:
                        # print(each_line.split('\t'))
                        self.save_data(each_line)
                    else:
                        print(f"index = {index}")
                        raise("data incomplete")
                else:
                    raise("reg error")
                        
                    
    def check_file(self):
        '''
        use for check file exists or not, if yes return True
        '''
        
        if os.path.exists(self.output_file):
            return True
        else:
            return False
    

    def make_fake_filemeta(self):
        '''
        use for write fake file meta 
        '''
        
        with open(self.output_file, "w") as f:
            f.write('{"name":"file_meta","raw_dumper_ver":"raw_dumper_v1_3","project_ver":"ESRTSD_generalProject_v1_0","machine_sn":"SXT261B60OA","api_ver":"SXT2_dev19.0","fw_ver":"SXT2_SMO_ver019_20211007","hw_ver":null,"sw_ver":"0.3.0-a1","app_name":"Enosim ESRTSD","user_sn":"7c7a274d47d046143b29109763b0debd31e82271c1671d46bd05150ba66c4a2d","organization":"enosim","reference_time":null,"l_date":"2022-04-01T13:49:56.395+08:00","channel_name":["_#mo_v#0","_#mo_v#0","_#mo_v#0","_#mo_v#0","_#mo_v#0","_#mo_v#0","_#mo_v#0","_#moin_v#0","_#moin_v#0","_#moin_v#0","_#moin_v#0","_#mo_v#0","_#mo_v#0","_#mo_v#0","_#rh_p#0","_#tm_c#0"], "preset_name":"sxt2_default","len_rounds":1,"full_task":["on_start","on_first_preset_voltage","on_first_waiting_initial","on_first_initial_end","on_second_preset_voltage","on_second_waiting_initial","on_second_initial_end","on_round_start","on_round_preset_voltage","on_round_waiting_initial","on_baseline_stable","on_collecting","on_stable","on_recovery","on_round_finished","on_finished"]}\n')
            f.write('{"name":"control_status","meta_index":-1,"l_date":"')
            for i in self.first_time:
                f.write(i)
            f.write('","status_flag":"on_start","subject_flag":"user","valve":0,"pump":1,"step_flag":null}\n')
            f.write('{"name":"control_status","meta_index":-1,"l_date":"')
            for i in self.first_time:
                f.write(i)
            f.write('","status_flag":"on_first_preset_voltage","subject_flag":"auto","valve":0,"pump":1,"step_flag":null}\n')
    
    def save_data(self,each_line):
        #{"name":"data","meta_index":-1,"l_date":"2022-04-01T11:24:37.736+08:00","channel":[1.58025,1.628,1.525,1.5405,1.55625,1.53975,1.575,3.238,3.46275,3.3645,3.418,1.90725,1.5195,1.976,0.520325,40.676193,0.33]}
        data_list = [f"{i}" for i in each_line.replace('\n', '').split('\t')[1:]]
        date = each_line.split('\t')[0].replace('/', '-').split(' ')[0]+"T"+each_line.split('\t')[0].replace('/', '-').split(' ')[-1]+".000+08:00"
        with open(self.output_file, "a") as f:
            f.write('{"name":"data","meta_index":-1,"l_date":"')
            for i in date:
                f.write(i)
            f.write('","channel":[')
            for index, i in enumerate(data_list):
                if index == len(data_list)-1:
                    f.write(i)
                else:
                    f.write(i)
                    f.write(',')
            f.write(']}\n')
            
            
    def find_first_time(self):
        with open(self.input_file, 'r') as f:
            content = f.readlines()
            for index, each_line in enumerate(content):
                if index == 0:
                    self.first_time = each_line.split('\t')[0].replace('/', '-').split(' ')[0]+"T"+each_line.split('\t')[0].replace('/', '-').split(' ')[-1]+".000+08:00"
                break
            
    def make_fake_preset_meta(self):
        #{"name":"preset_meta","meta_index":-1,"l_date":"2022-03-21T11:52:53.436+08:00","len_channel":17,"device_cfg":{"supply_voltage":5.0,"channel_biasing_resistance":[12469.0,10906.0,31219.0,26141.0,17547.0,23016.0,10125.0,3875.0,32000.0,8172.0,11688.0,2312.0,53875.0,2312.0,null,null,null],"channel_reference_c":[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],"channel_reference_voltage":[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],"preset_flow":[5.0],"channel_actual_gain":[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,null,null,null],"channel_preset_voltage":[1.5,1.5,1.5,1.5,1.5,1.5,1.5,3.5,3.5,3.5,3.5,1.5,1.5,1.5,null,null,null]},"critical":{"first_waiting_initial_stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":1800.0,"during":1.0},"second_waiting_initial_stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":10.0,"during":1.0},"round_waiting_initial_stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":30.0,"during":1.0},"baseline":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":60.0,"during":1.0},"stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":120.0,"during":1.0},"reacting":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":30.0,"during":1.0},"recovery":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":600.0,"during":1.0},"auto_stop_valve":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":4.0,"during":1.0},"slope_window_size":10,"threshold_ref_channel_indexes":[0,1]}}
        with open(self.output_file, "a") as f:
            f.write('{"name":"preset_meta","meta_index":-1,"l_date":"')
            for i in self.first_time:
                f.write(i)
            f.write('","len_channel":16,"device_cfg":{"supply_voltage":5.0,"channel_biasing_resistance":[')
            for i in self.rbias:
                f.write(str(i))
                f.write(',')
            f.write('null,null],"channel_reference_c":[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],"channel_reference_voltage":[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],"preset_flow":[5.0],"channel_actual_gain":[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,null,null],"channel_preset_voltage":[1.5,1.5,1.5,1.5,1.5,1.5,1.5,3.5,3.5,3.5,3.5,1.5,1.5,1.5,null,null]},"critical":{"first_waiting_initial_stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":1800.0,"during":1.0},"second_waiting_initial_stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":10.0,"during":1.0},"round_waiting_initial_stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":30.0,"during":1.0},"baseline":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":60.0,"during":1.0},"stable":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":120.0,"during":1.0},"reacting":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":30.0,"during":1.0},"recovery":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":600.0,"during":1.0},"auto_stop_valve":{"threshold_value":1.0,"threshold_rate":1.0,"timeout":4.0,"during":1.0},"slope_window_size":10,"threshold_ref_channel_indexes":[0,1]}}\n')
        