from structs import *
from ai import *

def selectBestUpgrade():
    if (player.HealthUpgrades <= player.CollectingUpgrades):
        return UpgradeType.MaximumHealth
    if (player.CollectingUpgrades <= player.CarryingUpgrades):
        return UpgradeType.CollectingSpeed
    if (player.CarryingUpgrades <= player.AttackUpgrades):
        return UpgradeType.CarryingCapacity
    if (player.AttackUpgrades <= player.DefenceUpgrades):
        return UpgradeType.AttackPower
    return UpgradeType.Defence
