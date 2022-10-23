records = []


class FileHeader:
    def __init__(self, parts):
        self.code = '01'
        self.sender = parts[1]
        self.recipient = parts[2]
        self.created_dt = parts[3]
        self.created_time = parts[4]
        self.file_identification_number = parts[5]
        self.physical_record_length = parts[6]
        self.block_size = parts[7]
        self.version = '2'

    def __repr__(self):
        return "FileHeader: [" \
               "record code: {0}" \
               ", sender: {1}" \
               ", next recipient: {2}" \
               ", created date: {3}" \
               ", created time: {4}" \
               ", file identification: {5}" \
               ", physical record length: {6}" \
               ", block size: {7}" \
               ", version: {8} ]".format(self.code
                                         , self.sender
                                         , self.recipient
                                         , self.created_dt
                                         , self.created_time
                                         , self.file_identification_number
                                         , self.physical_record_length
                                         , self.block_size, self.version)


class GroupHeader:
    def __init__(self, parts):
        self.code = '02'
        self.ultimate_receiver = parts[1]
        self.originator_identification = parts[2]
        self.group_status = ('Update', 1) if parts[3] == '1' \
            else ('Deletion', 2) if parts[3] == '2' \
            else ('Correction', 3) if parts[3] == '3' \
            else ('TestOnly', 4) if parts[3] == '4' \
            else None
        self.as_of_date = parts[4]
        self.as_of_time = parts[5]
        self.currency_code = parts[6]
        self.as_of_date_modifier = ('Interim Previous day data', 1) if parts[7] == '1' \
            else ('Final Previous day data', 1) if parts[7] == '2' \
            else ('Interim Same day data', 3) if parts[7] == '3' \
            else ('Final Same day data', 4) if parts[7] == '4' \
            else None

    def __repr__(self):
        return "Group Header[record code: {0}" \
               ", ultimate receiver: {1}" \
               ", originator identification: {2}" \
               ", group status: {3}" \
               ", as of date: {4}" \
               ", as of time: {5}" \
               ", currency code: {6}" \
               ", as of date modifier: {7} ]".format(self.code
                                                     , self.ultimate_receiver
                                                     , self.originator_identification
                                                     , self.group_status
                                                     , self.as_of_date
                                                     , self.as_of_time
                                                     , self.currency_code
                                                     , self.as_of_date_modifier)

class AccountIdentifier:
    def __init__(self):



def read_bai(filename):
    with open(filename, 'r') as f:
        for line in f:
            records.append(process_file(line.split(',')))
    print(records)


def process_file(parts):
    if parts[0] == '01': return FileHeader(parts)
    if parts[0] == '02': return GroupHeader(parts)
    if parts[0] == '03': return AccountIdentifier(parts)


if __name__ == '__main__':
    read_bai('./sample.bai2')
