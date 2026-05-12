class Judge:
    judges = []

    def add_judge(self):
        judge_id = int(input("Enter Judge ID: "))

        for judge in self.judges:
            if judge["judge_id"] == judge_id:
                print("Error: Judge ID already exists.")
                return

        name = input("Enter Judge Name: ")
        court_name = input("Enter Court Name: ")

        judge = {
            "judge_id": judge_id,
            "name": name,
            "court_name": court_name
        }

        self.judges.append(judge)
        print("Judge added successfully.")

    def get_all_judges(self):
        if len(self.judges) == 0:
            print("No judges found.")
        else:
            for judge in self.judges:
                print(judge)

    def get_judge_by_id(self):
        judge_id = int(input("Enter Judge ID: "))

        for judge in self.judges:
            if judge["judge_id"] == judge_id:
                print(judge)
                return

        print("Error: Judge does not exist.")

    def update_judge(self):
        judge_id = int(input("Enter Judge ID to update: "))

        for judge in self.judges:
            if judge["judge_id"] == judge_id:
                judge["name"] = input("Enter New Judge Name: ")
                judge["court_name"] = input("Enter New Court Name: ")
                print("Judge updated successfully.")
                return

        print("Error: Judge does not exist.")

    def delete_judge(self):
        judge_id = int(input("Enter Judge ID to delete: "))

        for judge in self.judges:
            if judge["judge_id"] == judge_id:
                self.judges.remove(judge)
                print("Judge deleted successfully.")
                return

        print("Error: Judge does not exist.")


class Client:
    clients = []

    def add_client(self):
        client_id = int(input("Enter Client ID: "))

        for client in self.clients:
            if client["client_id"] == client_id:
                print("Error: Client ID already exists.")
                return

        name = input("Enter Client Name: ")
        phone = input("Enter Phone Number: ")
        address = input("Enter Address: ")

        client = {
            "client_id": client_id,
            "name": name,
            "phone": phone,
            "address": address
        }

        self.clients.append(client)
        print("Client added successfully.")

    def get_all_clients(self):
        if len(self.clients) == 0:
            print("No clients found.")
        else:
            for client in self.clients:
                print(client)

    def get_client_by_id(self):
        client_id = int(input("Enter Client ID: "))

        for client in self.clients:
            if client["client_id"] == client_id:
                print(client)
                return

        print("Error: Client does not exist.")

    def update_client(self):
        client_id = int(input("Enter Client ID to update: "))

        for client in self.clients:
            if client["client_id"] == client_id:
                client["name"] = input("Enter New Client Name: ")
                client["phone"] = input("Enter New Phone Number: ")
                client["address"] = input("Enter New Address: ")
                print("Client updated successfully.")
                return

        print("Error: Client does not exist.")

    def delete_client(self):
        client_id = int(input("Enter Client ID to delete: "))

        for client in self.clients:
            if client["client_id"] == client_id:
                self.clients.remove(client)
                print("Client deleted successfully.")
                return

        print("Error: Client does not exist.")


class Lawyer:
    lawyers = []

    def add_lawyer(self):
        lawyer_id = int(input("Enter Lawyer ID: "))

        for lawyer in self.lawyers:
            if lawyer["lawyer_id"] == lawyer_id:
                print("Error: Lawyer ID already exists.")
                return

        name = input("Enter Lawyer Name: ")
        specialization = input("Enter Specialization: ")
        phone = input("Enter Phone Number: ")

        lawyer = {
            "lawyer_id": lawyer_id,
            "name": name,
            "specialization": specialization,
            "phone": phone
        }

        self.lawyers.append(lawyer)
        print("Lawyer added successfully.")

    def get_all_lawyers(self):
        if len(self.lawyers) == 0:
            print("No lawyers found.")
        else:
            for lawyer in self.lawyers:
                print(lawyer)

    def get_lawyer_by_id(self):
        lawyer_id = int(input("Enter Lawyer ID: "))

        for lawyer in self.lawyers:
            if lawyer["lawyer_id"] == lawyer_id:
                print(lawyer)
                return

        print("Error: Lawyer does not exist.")

    def update_lawyer(self):
        lawyer_id = int(input("Enter Lawyer ID to update: "))

        for lawyer in self.lawyers:
            if lawyer["lawyer_id"] == lawyer_id:
                lawyer["name"] = input("Enter New Lawyer Name: ")
                lawyer["specialization"] = input("Enter New Specialization: ")
                lawyer["phone"] = input("Enter New Phone Number: ")
                print("Lawyer updated successfully.")
                return

        print("Error: Lawyer does not exist.")

    def delete_lawyer(self):
        lawyer_id = int(input("Enter Lawyer ID to delete: "))

        for lawyer in self.lawyers:
            if lawyer["lawyer_id"] == lawyer_id:
                self.lawyers.remove(lawyer)
                print("Lawyer deleted successfully.")
                return

        print("Error: Lawyer does not exist.")


class Case:
    cases = []

    def add_case(self):
        case_id = int(input("Enter Case ID: "))

        for case in self.cases:
            if case["case_id"] == case_id:
                print("Error: Case ID already exists.")
                return

        client_id = int(input("Enter Client ID: "))
        judge_id = int(input("Enter Judge ID: "))
        title = input("Enter Case Title: ")
        status = input("Enter Case Status: ")
        filing_date = input("Enter Filing Date: ")

        case = {
            "case_id": case_id,
            "client_id": client_id,
            "judge_id": judge_id,
            "title": title,
            "status": status,
            "filing_date": filing_date
        }

        self.cases.append(case)
        print("Case added successfully.")

    def get_all_cases(self):
        if len(self.cases) == 0:
            print("No cases found.")
        else:
            for case in self.cases:
                print(case)

    def get_case_by_id(self):
        case_id = int(input("Enter Case ID: "))

        for case in self.cases:
            if case["case_id"] == case_id:
                print(case)
                return

        print("Error: Case does not exist.")

    def get_cases_by_client(self):
        client_id = int(input("Enter Client ID: "))
        found = False

        for case in self.cases:
            if case["client_id"] == client_id:
                print(case)
                found = True

        if found == False:
            print("Error: No case found for this client.")

    def get_cases_by_status(self):
        status = input("Enter Case Status: ")
        found = False

        for case in self.cases:
            if case["status"] == status:
                print(case)
                found = True

        if found == False:
            print("Error: No case found with this status.")

    def update_case(self):
        case_id = int(input("Enter Case ID to update: "))

        for case in self.cases:
            if case["case_id"] == case_id:
                case["client_id"] = int(input("Enter New Client ID: "))
                case["judge_id"] = int(input("Enter New Judge ID: "))
                case["title"] = input("Enter New Case Title: ")
                case["status"] = input("Enter New Case Status: ")
                case["filing_date"] = input("Enter New Filing Date: ")
                print("Case updated successfully.")
                return

        print("Error: Case does not exist.")

    def update_case_status(self):
        case_id = int(input("Enter Case ID: "))

        for case in self.cases:
            if case["case_id"] == case_id:
                case["status"] = input("Enter New Status: ")
                print("Case status updated successfully.")
                return

        print("Error: Case does not exist.")

    def delete_case(self):
        case_id = int(input("Enter Case ID to delete: "))

        for case in self.cases:
            if case["case_id"] == case_id:
                self.cases.remove(case)
                print("Case deleted successfully.")
                return

        print("Error: Case does not exist.")


class CaseLawyer:
    case_lawyers = []

    def assign_lawyer_to_case(self):
        case_id = int(input("Enter Case ID: "))
        lawyer_id = int(input("Enter Lawyer ID: "))

        for assignment in self.case_lawyers:
            if assignment["case_id"] == case_id and assignment["lawyer_id"] == lawyer_id:
                print("Error: This lawyer is already assigned to this case.")
                return

        assignment = {
            "case_id": case_id,
            "lawyer_id": lawyer_id
        }

        self.case_lawyers.append(assignment)
        print("Lawyer assigned to case successfully.")

    def get_all_assignments(self):
        if len(self.case_lawyers) == 0:
            print("No case-lawyer assignments found.")
        else:
            for assignment in self.case_lawyers:
                print(assignment)

    def get_lawyers_for_case(self):
        case_id = int(input("Enter Case ID: "))
        found = False

        for assignment in self.case_lawyers:
            if assignment["case_id"] == case_id:
                print(assignment)
                found = True

        if found == False:
            print("Error: No lawyer assigned to this case.")

    def get_cases_for_lawyer(self):
        lawyer_id = int(input("Enter Lawyer ID: "))
        found = False

        for assignment in self.case_lawyers:
            if assignment["lawyer_id"] == lawyer_id:
                print(assignment)
                found = True

        if found == False:
            print("Error: No case found for this lawyer.")

    def update_assignment(self):
        old_case_id = int(input("Enter Existing Case ID: "))
        old_lawyer_id = int(input("Enter Existing Lawyer ID: "))

        for assignment in self.case_lawyers:
            if assignment["case_id"] == old_case_id and assignment["lawyer_id"] == old_lawyer_id:
                assignment["case_id"] = int(input("Enter New Case ID: "))
                assignment["lawyer_id"] = int(input("Enter New Lawyer ID: "))
                print("Case-lawyer assignment updated successfully.")
                return

        print("Error: Case-lawyer assignment does not exist.")

    def delete_assignment(self):
        case_id = int(input("Enter Case ID: "))
        lawyer_id = int(input("Enter Lawyer ID: "))

        for assignment in self.case_lawyers:
            if assignment["case_id"] == case_id and assignment["lawyer_id"] == lawyer_id:
                self.case_lawyers.remove(assignment)
                print("Case-lawyer assignment deleted successfully.")
                return

        print("Error: Case-lawyer assignment does not exist.")


class TimelineEntry:
    timeline_entries = []

    def add_timeline_entry(self):
        timeline_id = int(input("Enter Timeline ID: "))

        for entry in self.timeline_entries:
            if entry["timeline_id"] == timeline_id:
                print("Error: Timeline ID already exists.")
                return

        case_id = int(input("Enter Case ID: "))
        date = input("Enter Date: ")
        description = input("Enter Description: ")

        entry = {
            "timeline_id": timeline_id,
            "case_id": case_id,
            "date": date,
            "description": description
        }

        self.timeline_entries.append(entry)
        print("Timeline entry added successfully.")

    def get_all_timeline_entries(self):
        if len(self.timeline_entries) == 0:
            print("No timeline entries found.")
        else:
            for entry in self.timeline_entries:
                print(entry)

    def get_timeline_for_case(self):
        case_id = int(input("Enter Case ID: "))
        result = []

        for entry in self.timeline_entries:
            if entry["case_id"] == case_id:
                result.append(entry)

        if len(result) == 0:
            print("Error: No timeline found for this case.")
        else:
            result.sort(key=lambda x: x["date"])
            for entry in result:
                print(entry)

    def update_timeline_entry(self):
        timeline_id = int(input("Enter Timeline ID to update: "))

        for entry in self.timeline_entries:
            if entry["timeline_id"] == timeline_id:
                entry["case_id"] = int(input("Enter New Case ID: "))
                entry["date"] = input("Enter New Date: ")
                entry["description"] = input("Enter New Description: ")
                print("Timeline entry updated successfully.")
                return

        print("Error: Timeline entry does not exist.")

    def delete_timeline_entry(self):
        timeline_id = int(input("Enter Timeline ID to delete: "))

        for entry in self.timeline_entries:
            if entry["timeline_id"] == timeline_id:
                self.timeline_entries.remove(entry)
                print("Timeline entry deleted successfully.")
                return

        print("Error: Timeline entry does not exist.")


class Journal:
    journals = []

    def add_journal_entry(self):
        journal_id = int(input("Enter Journal ID: "))

        for journal in self.journals:
            if journal["journal_id"] == journal_id:
                print("Error: Journal ID already exists.")
                return

        case_id = int(input("Enter Case ID: "))
        lawyer_id = int(input("Enter Lawyer ID: "))
        date = input("Enter Date: ")
        notes = input("Enter Notes: ")

        journal = {
            "journal_id": journal_id,
            "case_id": case_id,
            "lawyer_id": lawyer_id,
            "date": date,
            "notes": notes
        }

        self.journals.append(journal)
        print("Journal entry added successfully.")

    def get_all_journals(self):
        if len(self.journals) == 0:
            print("No journal entries found.")
        else:
            for journal in self.journals:
                print(journal)

    def get_journal_for_case(self):
        case_id = int(input("Enter Case ID: "))
        found = False

        for journal in self.journals:
            if journal["case_id"] == case_id:
                print(journal)
                found = True

        if found == False:
            print("Error: No journal found for this case.")

    def update_journal_entry(self):
        journal_id = int(input("Enter Journal ID to update: "))

        for journal in self.journals:
            if journal["journal_id"] == journal_id:
                journal["case_id"] = int(input("Enter New Case ID: "))
                journal["lawyer_id"] = int(input("Enter New Lawyer ID: "))
                journal["date"] = input("Enter New Date: ")
                journal["notes"] = input("Enter New Notes: ")
                print("Journal entry updated successfully.")
                return

        print("Error: Journal entry does not exist.")

    def delete_journal_entry(self):
        journal_id = int(input("Enter Journal ID to delete: "))

        for journal in self.journals:
            if journal["journal_id"] == journal_id:
                self.journals.remove(journal)
                print("Journal entry deleted successfully.")
                return

        print("Error: Journal entry does not exist.")


class Evidence:
    evidences = []

    def add_evidence(self):
        evidence_id = int(input("Enter Evidence ID: "))

        for evidence in self.evidences:
            if evidence["evidence_id"] == evidence_id:
                print("Error: Evidence ID already exists.")
                return

        case_id = int(input("Enter Case ID: "))
        evidence_name = input("Enter Evidence Name: ")
        description = input("Enter Description: ")
        file_path = input("Enter File Path: ")

        evidence = {
            "evidence_id": evidence_id,
            "case_id": case_id,
            "evidence_name": evidence_name,
            "description": description,
            "file_path": file_path
        }

        self.evidences.append(evidence)
        print("Evidence added successfully.")

    def get_all_evidence(self):
        if len(self.evidences) == 0:
            print("No evidence found.")
        else:
            for evidence in self.evidences:
                print(evidence)

    def get_evidence_for_case(self):
        case_id = int(input("Enter Case ID: "))
        found = False

        for evidence in self.evidences:
            if evidence["case_id"] == case_id:
                print(evidence)
                found = True

        if found == False:
            print("Error: No evidence found for this case.")

    def update_evidence(self):
        evidence_id = int(input("Enter Evidence ID to update: "))

        for evidence in self.evidences:
            if evidence["evidence_id"] == evidence_id:
                evidence["case_id"] = int(input("Enter New Case ID: "))
                evidence["evidence_name"] = input("Enter New Evidence Name: ")
                evidence["description"] = input("Enter New Description: ")
                evidence["file_path"] = input("Enter New File Path: ")
                print("Evidence updated successfully.")
                return

        print("Error: Evidence does not exist.")

    def delete_evidence(self):
        evidence_id = int(input("Enter Evidence ID to delete: "))

        for evidence in self.evidences:
            if evidence["evidence_id"] == evidence_id:
                self.evidences.remove(evidence)
                print("Evidence deleted successfully.")
                return

        print("Error: Evidence does not exist.")


class Payment:
    payments = []

    def add_payment(self):
        payment_id = int(input("Enter Payment ID: "))

        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                print("Error: Payment ID already exists.")
                return

        case_id = int(input("Enter Case ID: "))
        amount = float(input("Enter Amount: "))
        status = input("Enter Payment Status: ")
        payment_date = input("Enter Payment Date: ")

        payment = {
            "payment_id": payment_id,
            "case_id": case_id,
            "amount": amount,
            "status": status,
            "payment_date": payment_date
        }

        self.payments.append(payment)
        print("Payment added successfully.")

    def get_all_payments(self):
        if len(self.payments) == 0:
            print("No payments found.")
        else:
            for payment in self.payments:
                print(payment)

    def get_payments_for_case(self):
        case_id = int(input("Enter Case ID: "))
        found = False

        for payment in self.payments:
            if payment["case_id"] == case_id:
                print(payment)
                found = True

        if found == False:
            print("Error: No payment found for this case.")

    def update_payment(self):
        payment_id = int(input("Enter Payment ID to update: "))

        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                payment["case_id"] = int(input("Enter New Case ID: "))
                payment["amount"] = float(input("Enter New Amount: "))
                payment["status"] = input("Enter New Payment Status: ")
                payment["payment_date"] = input("Enter New Payment Date: ")
                print("Payment updated successfully.")
                return

        print("Error: Payment does not exist.")

    def update_payment_status(self):
        payment_id = int(input("Enter Payment ID: "))

        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                payment["status"] = input("Enter New Payment Status: ")
                print("Payment status updated successfully.")
                return

        print("Error: Payment does not exist.")

    def delete_payment(self):
        payment_id = int(input("Enter Payment ID to delete: "))

        for payment in self.payments:
            if payment["payment_id"] == payment_id:
                self.payments.remove(payment)
                print("Payment deleted successfully.")
                return

        print("Error: Payment does not exist.")

    def get_total_paid_amount(self):
        case_id = int(input("Enter Case ID: "))
        total = 0

        for payment in self.payments:
            if payment["case_id"] == case_id and payment["status"] == "Paid":
                total = total + payment["amount"]

        print("Total Paid Amount:", total)


judge_obj = Judge()
client_obj = Client()
lawyer_obj = Lawyer()
case_obj = Case()
case_lawyer_obj = CaseLawyer()
timeline_obj = TimelineEntry()
journal_obj = Journal()
evidence_obj = Evidence()
payment_obj = Payment()


while True:
    print("\n~~~~~~~~~~ Law Firm MANAGEMENT SYSTEM ~~~~~~~~~~")

    print("\n~~~ Judge Menu ~~~")
    print("1. Add Judge")
    print("2. View All Judges")
    print("3. Search Judge By ID")
    print("4. Update Judge")
    print("5. Delete Judge")

    print("\n~~~ Client Menu ~~~")
    print("6. Add Client")
    print("7. View All Clients")
    print("8. Search Client By ID")
    print("9. Update Client")
    print("10. Delete Client")

    print("\n~~~ Lawyer Menu ~~~")
    print("11. Add Lawyer")
    print("12. View All Lawyers")
    print("13. Search Lawyer By ID")
    print("14. Update Lawyer")
    print("15. Delete Lawyer")

    print("\n~~~ Case Menu ~~~")
    print("16. Add Case")
    print("17. View All Cases")
    print("18. Search Case By ID")
    print("19. Search Cases By Client")
    print("20. Search Cases By Status")
    print("21. Update Case")
    print("22. Update Case Status")
    print("23. Delete Case")

    print("\n~~~ Case Lawyer Menu ~~~")
    print("24. Assign Lawyer To Case")
    print("25. View All Assignments")
    print("26. Get Lawyers For Case")
    print("27. Get Cases For Lawyer")
    print("28. Update Assignment")
    print("29. Delete Assignment")

    print("\n~~~ Timeline Menu ~~~")
    print("30. Add Timeline Entry")
    print("31. View All Timeline Entries")
    print("32. Get Timeline For Case")
    print("33. Update Timeline Entry")
    print("34. Delete Timeline Entry")

    print("\n~~~ Journal Menu ~~~")
    print("35. Add Journal Entry")
    print("36. View All Journals")
    print("37. Get Journal For Case")
    print("38. Update Journal Entry")
    print("39. Delete Journal Entry")

    print("\n~~~ Evidence Menu ~~~")
    print("40. Add Evidence")
    print("41. View All Evidence")
    print("42. Get Evidence For Case")
    print("43. Update Evidence")
    print("44. Delete Evidence")

    print("\n~~~ Payment Menu ~~~")
    print("45. Add Payment")
    print("46. View All Payments")
    print("47. Get Payments For Case")
    print("48. Update Payment")
    print("49. Update Payment Status")
    print("50. Delete Payment")
    print("51. Get Total Paid Amount")

    print("\n0. Exit")

    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        judge_obj.add_judge()
    elif choice == 2:
        judge_obj.get_all_judges()
    elif choice == 3:
        judge_obj.get_judge_by_id()
    elif choice == 4:
        judge_obj.update_judge()
    elif choice == 5:
        judge_obj.delete_judge()

    elif choice == 6:
        client_obj.add_client()
    elif choice == 7:
        client_obj.get_all_clients()
    elif choice == 8:
        client_obj.get_client_by_id()
    elif choice == 9:
        client_obj.update_client()
    elif choice == 10:
        client_obj.delete_client()

    elif choice == 11:
        lawyer_obj.add_lawyer()
    elif choice == 12:
        lawyer_obj.get_all_lawyers()
    elif choice == 13:
        lawyer_obj.get_lawyer_by_id()
    elif choice == 14:
        lawyer_obj.update_lawyer()
    elif choice == 15:
        lawyer_obj.delete_lawyer()

    elif choice == 16:
        case_obj.add_case()
    elif choice == 17:
        case_obj.get_all_cases()
    elif choice == 18:
        case_obj.get_case_by_id()
    elif choice == 19:
        case_obj.get_cases_by_client()
    elif choice == 20:
        case_obj.get_cases_by_status()
    elif choice == 21:
        case_obj.update_case()
    elif choice == 22:
        case_obj.update_case_status()
    elif choice == 23:
        case_obj.delete_case()

    elif choice == 24:
        case_lawyer_obj.assign_lawyer_to_case()
    elif choice == 25:
        case_lawyer_obj.get_all_assignments()
    elif choice == 26:
        case_lawyer_obj.get_lawyers_for_case()
    elif choice == 27:
        case_lawyer_obj.get_cases_for_lawyer()
    elif choice == 28:
        case_lawyer_obj.update_assignment()
    elif choice == 29:
        case_lawyer_obj.delete_assignment()

    elif choice == 30:
        timeline_obj.add_timeline_entry()
    elif choice == 31:
        timeline_obj.get_all_timeline_entries()
    elif choice == 32:
        timeline_obj.get_timeline_for_case()
    elif choice == 33:
        timeline_obj.update_timeline_entry()
    elif choice == 34:
        timeline_obj.delete_timeline_entry()

    elif choice == 35:
        journal_obj.add_journal_entry()
    elif choice == 36:
        journal_obj.get_all_journals()
    elif choice == 37:
        journal_obj.get_journal_for_case()
    elif choice == 38:
        journal_obj.update_journal_entry()
    elif choice == 39:
        journal_obj.delete_journal_entry()

    elif choice == 40:
        evidence_obj.add_evidence()
    elif choice == 41:
        evidence_obj.get_all_evidence()
    elif choice == 42:
        evidence_obj.get_evidence_for_case()
    elif choice == 43:
        evidence_obj.update_evidence()
    elif choice == 44:
        evidence_obj.delete_evidence()

    elif choice == 45:
        payment_obj.add_payment()
    elif choice == 46:
        payment_obj.get_all_payments()
    elif choice == 47:
        payment_obj.get_payments_for_case()
    elif choice == 48:
        payment_obj.update_payment()
    elif choice == 49:
        payment_obj.update_payment_status()
    elif choice == 50:
        payment_obj.delete_payment()
    elif choice == 51:
        payment_obj.get_total_paid_amount()

    elif choice == 0:
        print("Program closed successfully.")
        break

    else:
        print("Invalid choice. Please try again.")