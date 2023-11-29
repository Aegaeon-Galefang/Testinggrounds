# In[29]:


#protocol version for serial dilution

from opentrons import protocol_api

metadata = {
    "apiLevel": "2.15",
    "protocolName": "Serial Dilutions",
    "description": "This protocol is the outcome of the iGEM Serial Dilution Standard Protocol",
    "author": "Ryan Sze et al"
    }

def run(protocol: protocol_api.ProtocolContext):
    #define what goes in each position of opentrons layout. Add custom labware in labware file of .opentrons file location
    #Labware
    plate = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    reservoir = protocol.load_labware('4ti0131_12_reservoir_21000ul', 3) #A1 is PBS, A2 is fluorescin stock

    #pipettes
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_1]) #uses multi-pipette
    protocol.max_speeds['Z'] = 10
    
    
    p300_multi.distribute(100, reservoir.wells('A1'), 
                      plate.wells('A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12')) #Distributing PBS
    p300_multi.distribute(100, reservoir.wells('A2'), 
                          plate.wells('A1', 'A2')) #Distributing fluorescin into stock reference wells and first dilutions

    p300_multi.pick_up_tip()
    for i in range(10):
        arrival = 'A' + str(i+1)
        destination = 'A' + str(i+2)
        p300_multi.transfer(100, plate[arrival], plate[destination], mix_before=(3,50), 
                  touch_tip=True, blow_out=True, blowout_location='destination well', new_tip='never') #Serial dilution transfers

    p300_multi.aspirate(100, plate['A11'])
    p300_multi.drop_tip() #Removal of final 100 microliters in A11

