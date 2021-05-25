"""Main module."""


"""" generate test data csv - for sql tests which do not include data """

import uuid, arrow, random
import pandas as pd

# given a json of values for rows etc?

test_data_spec = {
    "data_spec": [
        {
            "name": "event_id",
            "type": "guid",
            "overlap": False
        },
        {
            "name": "timestamp",
            "type": "timestamp",
            "overlap": True,
            "values": {
                "format": "X",
                "startrange": "2021-01-01",
                "endrange": "2021-06-01"
            }
        },
        {
            "name": "user_id",
            "type": "user_id",
            "overlap": True,
            "values": {
                "overlap": .9
            }
        },
        {
            "name": "design_category",
            "type": "list",
            "overlap": True,
            "values": [ "birthday invitation","business card","festival poster"]
        }

    ],
    "rows": 100000
}

rows = test_data_spec["rows"]

def generate_guid(rows,dict_object):
    rows_returned = []

    for each_row in range(0,rows):
        rows_returned.append(str(uuid.uuid4()))
    return rows_returned


def generate_timestamp(rows,dict_object):

    rows_returned = []
    settings = dict_object
    # settings = {
    #         "name": "timestamp",
    #         "type": "timestamp",
    #         "overlap": True,
    #         "values": {
    #             "format": "X",
    #             "startrange": "2021-05-01",
    #             "endrange": "2021-07-01"
    #         }
    #     }
    
    start_date = arrow.get(settings["values"]["startrange"]).format(settings["values"]["format"])
    end_date = arrow.get(settings["values"]["endrange"]).format(settings["values"]["format"])

    print(start_date,end_date)

    for each_row in range(0,rows):
        rows_returned.append(random.randrange(int(start_date),int(end_date)) )
    return rows_returned



def generate_user_id(rows, dict_object):
    # random.seed(100)
    settings = dict_object
    # {
    #         "name": "user_id",
    #         "type": "user_id",
    #         "overlap": True,
    #         "values": {
    #             "overlap": .9
    #         }
    #     },

    if dict_object["overlap"] == True:
        overlap_perc = dict_object["values"]["overlap"]
    else:
        overlap_perc = 0

    def generate_single_user():
        return "user_"+str(uuid.uuid4())

    #do simple math to generate a base set of users based on overlap
    def generate_base_users(rows,overlap_perc):
        """ create a base list we can use for overlapping users """
        users_to_create = int(rows * overlap_perc)
        
        user_list = []
        
        for each_user in range(0,users_to_create):
            user_list.append(generate_single_user() )
        return user_list

    def create_overlapping_user_list(rows, overlap_perc):
        """ pull this together to do this """
        output_user_ids = []
        base_user_ids = generate_base_users(rows,overlap_perc)

        for each_new_user in range( 0, rows):
            random_int = random.randint(1,100)
            overlap_threshhold = (100- (100*overlap_perc) )
            if random_int >= overlap_threshhold:
                # print(f"choosing overlap, {random_int} more than {overlap_threshhold}")
                #falls within overlap setting. get from list
                output_user_ids.append(random.choice(base_user_ids))
            else:
                # print(f"no overlap, {random_int} not more than {overlap_threshhold}")
                output_user_ids.append(generate_single_user())
        return output_user_ids
    
    return create_overlapping_user_list(rows,overlap_perc)

  
def generate_from_list(rows, dict_object):
    # {
    #         "name": "design_category",
    #         "type": "list",
    #         "overlap": True,
    #         "values": [ "birthday invitation","business card","festival poster"]
    #     }
    settings = dict_object
    list_to_use = settings[ "values"]

    output_list = []
    for each_row in range(0,rows):
        output_list.append(random.choice(list_to_use))
    
    return output_list


def create_test_data_from_spec(input_dict):
    """iterates through spec dict and outputs test data """

    rows = input_dict["rows"]

    def detect_dict_element_type(rows,dict_object):
        try: 
            dict_field_type = dict_object["type"]

            if dict_field_type == "timestamp":
                return generate_timestamp(rows=rows,dict_object = dict_object)
            elif dict_field_type == "guid":
                return generate_guid(rows=rows, dict_object=dict_object)
            elif dict_field_type == "user_id":
                return generate_user_id(rows=rows, dict_object=dict_object)
            elif dict_field_type == "list":
                return generate_from_list(rows=rows,dict_object=dict_object)
            else:
                raise Exception(f"{dict_field_type} not supported")

        except Exception as e:
            raise Exception(e)

    def get_columns(input_dict):
        """build the columns for the df"""
        column_list = []
        for each_line in input_dict["data_spec"]:
            column_list.append(each_line["name"])
        return column_list


    df_columns = get_columns(input_dict)
    df = pd.DataFrame(columns=df_columns)

    for each_line in input_dict["data_spec"]:
        column_data = detect_dict_element_type(rows,each_line)
        column_header = each_line["name"]
        df[column_header] = column_data


    # df = pd.DataFrame(columns=["event_id", "timestamp", "user_id", "design_category"])
    # df["event_id"] = generate_guid(rows)
    # df["timestamp"] = generate_timestamp(rows)
    # df["user_id"] = generate_user_id(rows,.5)
    # df["design_category"] = generate_from_list(rows)

    df.to_csv("test_data_output.csv", index=False)
    print("dates exported")



create_test_data_from_spec(test_data_spec)

    