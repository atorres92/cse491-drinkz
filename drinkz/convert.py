def convert_to_ml( amt ):
    if amt[-2:] == 'ml':
        amtNum = float(amt.strip('ml'))
    elif amt[-2:] == 'oz':
        amtNum = float(amt.strip('oz'))
        amtNum *= 29.5735
    elif amt[-5:] == 'liter':
        amtNum = float(amt.strip('liter'))
        amtNum *= 1000
    elif amt[-6:] == 'gallon':
        amtNum = float(amt.strip('gallon'))
        amtNum *= 3785.41
    else:
        amtNum = 0
    return amtNum
        
    
