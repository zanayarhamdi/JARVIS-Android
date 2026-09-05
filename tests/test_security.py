import unittest
from security.permission_checker import PermissionChecker, Permission
from security.risk_assessor import RiskAssessor, RiskLevel

class TestSecurity(unittest.TestCase):
    
    def setUp(self):
        self.permission_checker = PermissionChecker()
        self.risk_assessor = RiskAssessor()
    
    def test_permissions(self):
        """Test permission checking"""
        self.assertTrue(
            self.permission_checker.has_permission('admin', Permission.DELETE_FILES)
        )
        self.assertFalse(
            self.permission_checker.has_permission('user', Permission.INSTALL_PACKAGES)
        )
    
    def test_risk_assessment(self):
        """Test risk assessment"""
        assessment = self.risk_assessor.assess_risk('delete')
        self.assertTrue(assessment.get('requires_confirmation'))
        self.assertEqual(assessment.get('risk_level'), 'HIGH')
    
    def test_action_permission(self):
        """Test action permissions"""
        self.assertTrue(
            self.permission_checker.can_perform_action('read_file', 'user')
        )
        self.assertFalse(
            self.permission_checker.can_perform_action('install_package', 'user')
        )

if __name__ == '__main__':
    unittest.main()
