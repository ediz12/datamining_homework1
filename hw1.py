from pyparsing import OneOrMore, nestedExpr
import json
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances

class ParseDataSet(object):
    def __init__(self):
        self.filename = "dataset.data"
        self.dataset = {}
        # self.load_dataset(self.filename)
        # self.revise_dataset()
        self.load_json()
        self.save_json()
        self.print_data()

    def load_dataset(self, filename):
        # LOAD THE LISP DATA
        with open(filename, "r") as f:
            dataset = OneOrMore(nestedExpr()).parseString("".join(f.readlines()))

        definstance = 0
        defprop = 0
        duplicate = 0

        for data in dataset:
            if data[0].lower() == "def-instance":
                definstance += 1

                university = data[1].replace("-", " ").title()
                if university[-1].isnumeric():
                    university = university[:-1]

                if university in self.dataset.keys():
                    # COUNT DUPES
                    duplicate += 1

                else:
                    # INITIALIZE NEEDED DATA
                    self.dataset[university] = {
                        "state": "N/A",
                        "location": "N/A",
                        "control": "N/A",
                        "no-of-students": "N/A",
                        "male:female": "N/A",
                        "student:faculty": "N/A",
                        "sat verbal": "N/A",
                        "sat math": "N/A",
                        "expenses": "N/A",
                        "percent-financial-aid": "N/A",
                        "no-applicants": "N/A",
                        "percent-admittance": "N/A",
                        "percent-enrolled": "N/A",
                        "academics scale:1-5": "N/A",
                        "social scale:1-5": "N/A",
                        "quality-of-life scale:1-5": "N/A",
                        "academic-emphasis": []
                    }

                for info in data[2:]:
                    # MAKE IT MORE READABLE IN A JSON FORMAT
                    info_type, info_data = " ".join(info[:-1]).lower(), info[-1].capitalize()

                    if info_type == "academic-emphasis":
                        # ADD A LIST OF CLASSES TO THE DATA
                        if info_data not in self.dataset[university]["academic-emphasis"]:
                            self.dataset[university]["academic-emphasis"].append(info_data)

                    else:
                        if info_type in ("male:female", "student:faculty"):
                            try:
                                # ADD BOTH MALE/FEMALE and STUDENT/FACULTY RATIO TO THE CLASSES
                                _, first, second = info_data.split(":")
                                ratio = "%.2f" % ((float(first) / (float(second) + float(first))) * 100)
                            except:
                                if info_type == "male:female":
                                    # SET AN EQUAL VALUE OF M/F RATIO IF IT DOES NOT EXIST
                                    ratio = "50.00"
                                else:
                                    ratio = "N/A"

                            self.dataset[university][info_type] = ratio

                        elif info_type == "state":
                            # THERE ARE NO PROBLEMS WITH STATE, JUST ADD
                            self.dataset[university][info_type] = info_data

                        elif info_type == "location":
                            # DONE: LOCATION INFORMATION. THERE ARE N/A VALUES. PUT MOST COMMON ONE
                            if info_data.lower() != "n/a":
                                self.dataset[university][info_type] = info_data

                        elif info_type == "control":
                            # DONE: CONTROL INFORMATION. THERE ARE N/A VALUES. PUT MOST COMMON ONE

                            if info_data.lower() != "n/a":
                                self.dataset[university][info_type] = info_data

                        elif info_type == "no-of-students":
                            # THERE ARE NO PROBLEMS WITH NUMBER OF STUDENTS, JUST ADD

                            info_data = info_data.replace("Thous:", "")

                            if info_data == "5-":
                                info_data = "0-5000"
                            elif info_data == "5-10":
                                info_data = "5000-10000"
                            elif info_data == "10-15":
                                info_data = "10000-15000"
                            elif info_data == "15-20":
                                info_data = "15000-20000"
                            elif info_data == "20+":
                                info_data = "20000+"

                            self.dataset[university][info_type] = info_data

                        elif info_type in ("sat math", "sat verbal"):
                            # DONE: SAT INFORMATION. THERE ARE N/A VALUES. PUT AVERAGE
                            if info_data.lower() != "n/a":
                                self.dataset[university][info_type] = info_data

                        elif info_type == "expenses":
                            info_data = info_data.replace("Thous$:", "")

                            if info_data == "4-":
                                info_data = "0-4000"
                            elif info_data == "4-7":
                                info_data = "4000-7000"
                            elif info_data == "7-10":
                                info_data = "7000-10000"
                            elif info_data == "10+":
                                info_data = "10000+"

                            self.dataset[university][info_type] = info_data

                        elif info_type == "percent-financial-aid":
                            # DONE: SET 0 IF N/A, SINCE IT MEANS THERE'S NO AID

                            self.dataset[university][info_type] = info_data

                        elif info_type == "no-applicants":
                            # DONE: SET THE MODE OF NO-APPLICANTS FOR N/A

                            info_data = info_data.replace("Thous:", "")

                            if info_data == "4-":
                                info_data = "0-4000"
                            elif info_data == "4-7":
                                info_data = "4000-7000"
                            elif info_data == "7-10":
                                info_data = "7000-10000"
                            elif info_data == "10-13":
                                info_data = "10000-13000"
                            elif info_data == "13-17":
                                info_data = "13000-17000"
                            elif info_data == "17+":
                                info_data = "17000+"

                            self.dataset[university][info_type] = info_data

                        elif info_type == "percent-admittance":
                            # DONE: ADMITTANCE INFORMATION. THERE ARE N/A VALUES. PUT 100.
                            if info_data.lower() != "n/a":
                                self.dataset[university][info_type] = info_data

                        elif info_type == "percent-enrolled":
                            # DONE: ADMITTANCE INFORMATION. THERE ARE N/A VALUES. PUT PERCENTAGE ADMIT?
                            if info_data.lower() != "n/a":
                                self.dataset[university][info_type] = info_data

                        elif info_type in ("academics scale:1-5", "social scale:1-5", "quality-of-life scale:1-5"):
                            # DONE: SCALE RATIO OF UNIVERSITY. THERE ARE N/A VALUES. PUT 3 FOR THEM.

                            if info_data.lower() != "n/a":
                                self.dataset[university][info_type] = info_data

                        elif info_type == "":
                            # IF EMPTY TYPE, IGNORE THE DATA. THIS IS BECAUSE WE SPLIT BY SPACES IN THE DATA.
                            # SO WE IGNORE IT TO AVOID GETTING THEM ADDED.
                            pass
                        else:
                            self.dataset[university][info_type] = info_data

            else:
                defprop += 1
                # print(data)

        print("Given dataset #: {0}, Our dataset #:  {1}, Defdrop #: {2}, "
              "Definstance #: {3}, Duplicate #: {4}, Total #: {5}".format(
            len(dataset), len(self.dataset), defprop, definstance, duplicate, len(self.dataset) + duplicate))

    def revise_dataset(self):
        for university, data in self.dataset.items():
            for data_type, data_info in data.items():
                if data_type != "academic-emphasis":
                    if data_info.lower() in ("n/a", "na", "act-15", "act-21"):
                        if data_type in ("control", "location", "no-applicants"):
                            # MODE MAKES MOST SENSE
                            self.dataset[university][data_type] = self.find_mode(data_type)[0]
                        elif data_type in ("academics scale:1-5", "social scale:1-5", "quality-of-life scale:1-5"):
                            # PUT THE AVERAGE VALUE OF 1-5, THAT IS 3
                            self.dataset[university][data_type] = "3"
                        elif data_type == "percent-financial-aid":
                            # N/A MEANS NO FINANCIAL AID, THUS 0
                            self.dataset[university][data_type] = "0"
                        elif data_type == "percent-admittance":
                            # WE ASSUME EVERYONE WHO APPLIED IS IN TO HELP CALCULATION EASIER
                            self.dataset[university][data_type] = "100"
                        elif data_type == "percent-enrolled":
                            first, second = self.dataset[university]["no-applicants"].split("-")
                            no_applicants = "%.2f" % (((float(first) + float(second)) / 2) * 100)

                            first, second = self.dataset[university]["no-of-students"].split("-")
                            no_students = "%.2f" % (((float(first) + float(second)) / 2) * 100)

                            data_info = ((float(no_students) / 4) / float(no_applicants)) * 100

                            self.dataset[university][data_type] = data_info
                        elif data_type in ("sat math", "sat verbal", "student:faculty"):
                            # FIND THE AVERAGE FOR N/A NUMBERS
                            self.dataset[university][data_type] = self.find_mean(data_type)

    def get_all_data(self, data_type):
        n = []
        for university, data in self.dataset.items():
            n.append(float(self.dataset[university][data_type]))
        return n

    def find_mode(self, data_type):
        count_list = {}

        for university, data in self.dataset.items():
            value = self.dataset[university][data_type]

            if str(value).lower() != "n/a":
                if value in count_list:
                    count_list[value] += 1
                else:
                    count_list[value] = 1

        return sorted(count_list.items(), key=lambda x: x[1], reverse=True)[0]

    def find_mean(self, data_type):
        count = 0
        total = 0

        for university, data in self.dataset.items():
            value = self.dataset[university][data_type]

            try:
                total += float(value)
                count += 1
            except ValueError:
                pass

        return "%.2f" % (total / count)

    def find_standard_dev(self, data_type):
        mean = float(self.find_mean(data_type))
        count = 0
        total = 0

        for university, data in self.dataset.items():
            value = float(self.dataset[university][data_type])
            """print("Got value: " + str(value))
            print("(value - mean): " + str(value - mean))
            print("(value - mean) ** 2: " + str((value - mean) ** 2))"""
            total = total + ((value - mean) ** 2)
            # print(total, value, mean)
            count += 1

        return "%.2f" % ((total / (count - 1)) ** (1 / 2))

    def find_median(self, data_type):
        n = []
        for university, data in self.dataset.items():
            n.append(float(self.dataset[university][data_type]))

        index = (len(n) - 1) // 2
        n.sort()
        if len(n) % 2 == 0:
            return n[index]
        else:
            return (n[index] + n[index + 1]) / 2

    def find_skewness(self, data_type):
        mean = float(self.find_mean(data_type))
        median = self.find_median(data_type)
        sd = float(self.find_standard_dev(data_type))
        return "%.2f" % ((3 * (mean - median)) / sd)

    def calculate_data(self, data_type):
        mean = self.find_mean(data_type)
        sd = self.find_standard_dev(data_type)
        mode = self.find_mode(data_type)
        skew = self.find_skewness(data_type)

        return {"mean": mean,
                "standard deviation": sd,
                "mode": mode[0],
                "skewness": skew
                }

    def print_stats(self, data):
        print("\t\tMean: {0}\tStandard deviation: {1}\tMode: {2}\tSkewness: {3}".format(data["mean"],
                                                                                       data["standard deviation"],
                                                                                       data["mode"],
                                                                                       data["skewness"]))
    def print_data(self):
        print("Numerical attributes:")
        print("\tMale to female percentage statistics:")
        self.print_stats(self.calculate_data("male:female"))
        print("\n")
        print("\tStudent to teacher percentage statistics:")
        self.print_stats(self.calculate_data("student:faculty"))
        print("\n")
        print("\tSAT verbal statistics:")
        self.print_stats(self.calculate_data("sat verbal"))
        print("\n")
        print("\tSAT mathematical statistics:")
        self.print_stats(self.calculate_data("sat math"))
        print("\n")
        print("\tFinancial aid percentage of the university statistics:")
        self.print_stats(self.calculate_data("percent-financial-aid"))
        print("\n")
        print("\tPercentage of admitted students to the university statistics:")
        self.print_stats(self.calculate_data("percent-admittance"))
        print("\n")
        print("\tPercentage of the enrolled students to the university statistics:")
        self.print_stats(self.calculate_data("percent-enrolled"))
        print("\n")
        print("\tAcademics life on a scale of 1 to 5 statistics:")
        self.print_stats(self.calculate_data("academics scale:1-5"))
        print("\n")
        print("\tSocial life on a scale of 1 to 5 statistics:")
        self.print_stats(self.calculate_data("social scale:1-5"))
        print("\n")
        print("\tQuality of life on a scale of 1 to 5 statistics:")
        self.print_stats(self.calculate_data("quality-of-life scale:1-5"))
        print("\n\n")
        print("Categorical variables:")
        state, n = self.find_mode("state")
        print("\tMost universities are in {0} state ({1} universities)".format(state, n))
        location, n = self.find_mode("location")
        print("\tMost universities are in {0} location ({1} universities)".format(location, n))
        control, n = self.find_mode("control")
        print("\tMost universities are {0} ({1} universities)".format(control, n))
        stu, n = self.find_mode("no-of-students")
        print("\tStudents numbers mostly vary in {0} ({1} universities)".format(stu, n))
        expenses, n = self.find_mode("expenses")
        print("\tMost universities' expenses are in {0}$ ({1} universities)".format(expenses, n))
        apps, n = self.find_mode("no-applicants")
        print("\tMost universities have {0} applicants ({1} universities)".format(apps, n))

        self.plot_histogram("Male Female Ratio", "Probability", self.get_all_data("male:female"), True)
        self.plot_histogram("Student Faculty Ratio", "Probability", self.get_all_data("student:faculty"))
        self.plot_histogram("SAT Verbal Scores", "Probability", self.get_all_data("sat verbal"))
        self.plot_histogram("SAT Math Scores", "Probability", self.get_all_data("sat math"))
        self.plot_histogram("Financial Aid Percentages (%)", "Probability", self.get_all_data("percent-financial-aid"))
        self.plot_histogram("Admittance Percentage (%)", "Probability", self.get_all_data("percent-admittance"))
        self.plot_histogram("Enrolled Percentage (%)", "Probability", self.get_all_data("percent-enrolled"))

        self.scatter_plot_academics()

    def plot_histogram(self, title, y_label, numbers, discrete=False):
        plt.hist(numbers, 100, histtype="stepfilled")
        plt.title(title)
        plt.xlabel(title)
        plt.ylabel(y_label)
        if discrete == True:
            plt.grid = True

        plt.show()

    def scatter_plot_academics(self):
        dict1 = {}

        for university, data in self.dataset.items():
            for lecture in self.dataset[university]["academic-emphasis"]:
                try:
                    dict1[lecture] += 1
                except:
                    dict1[lecture] = 1

        x = list(dict1.values())

        z = [[x[i], x[i]] for i in range(len(x))]

        print(euclidean_distances(z))


    def load_json(self):
        with open("json_data.json", "r") as f:
            self.dataset = json.load(f)

    def save_json(self):
        with open("json_data.json", "w") as f:
            json.dump(self.dataset, f, indent=4)


ParseDataSet()
