class DeployController:

    def deploy(self, old_system, new_system):

        # hot swap (upgradeable to blue-green deployment)
        old_system.clear()
        old_system.update(new_system)

        return "system upgraded"
