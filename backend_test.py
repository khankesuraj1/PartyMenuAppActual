import requests
import sys
from datetime import datetime

class PartyMenuAPITester:
    def __init__(self, base_url="https://5fc0f851-decb-4ac1-8ed7-d0c749251207.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = "test_user_123"

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, list) and len(response_data) > 0:
                        print(f"   Response: Found {len(response_data)} items")
                    elif isinstance(response_data, dict):
                        print(f"   Response keys: {list(response_data.keys())}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")

            return success, response.json() if response.status_code < 400 else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_get_all_dishes(self):
        """Test getting all dishes"""
        return self.run_test("Get All Dishes", "GET", "dishes", 200)

    def test_get_dishes_by_meal_type(self):
        """Test filtering dishes by meal type"""
        meal_types = ["STARTER", "MAIN_COURSE", "DESSERT", "SIDES"]
        results = []
        
        for meal_type in meal_types:
            success, response = self.run_test(
                f"Get {meal_type} Dishes", 
                "GET", 
                "dishes", 
                200, 
                params={"meal_type": meal_type}
            )
            results.append(success)
            
            if success and response:
                # Verify all returned dishes are of correct meal type
                for dish in response:
                    if dish.get("mealType") != meal_type:
                        print(f"❌ Meal type filter failed: Expected {meal_type}, got {dish.get('mealType')}")
                        return False
                        
        return all(results)

    def test_get_dishes_by_type(self):
        """Test filtering dishes by veg/non-veg"""
        dish_types = ["VEG", "NON_VEG"]
        results = []
        
        for dish_type in dish_types:
            success, response = self.run_test(
                f"Get {dish_type} Dishes", 
                "GET", 
                "dishes", 
                200, 
                params={"dish_type": dish_type}
            )
            results.append(success)
            
            if success and response:
                # Verify all returned dishes are of correct type
                for dish in response:
                    if dish.get("type") != dish_type:
                        print(f"❌ Dish type filter failed: Expected {dish_type}, got {dish.get('type')}")
                        return False
                        
        return all(results)

    def test_search_dishes(self):
        """Test searching dishes by name"""
        search_terms = ["Paneer", "Chicken", "Cake"]
        results = []
        
        for term in search_terms:
            success, response = self.run_test(
                f"Search for '{term}'", 
                "GET", 
                "dishes", 
                200, 
                params={"search": term}
            )
            results.append(success)
            
            if success and response:
                # Verify search results contain the search term
                for dish in response:
                    if term.lower() not in dish.get("name", "").lower():
                        print(f"❌ Search failed: '{term}' not found in '{dish.get('name')}'")
                        return False
                        
        return all(results)

    def test_get_meal_types(self):
        """Test getting meal types"""
        success, response = self.run_test("Get Meal Types", "GET", "meal-types", 200)
        
        if success and response:
            expected_types = ["STARTER", "MAIN_COURSE", "DESSERT", "SIDES"]
            actual_types = response.get("meal_types", [])
            
            if set(expected_types) != set(actual_types):
                print(f"❌ Meal types mismatch: Expected {expected_types}, got {actual_types}")
                return False
                
        return success

    def test_dish_ingredients(self):
        """Test getting dish ingredients"""
        # Test with dishes that have ingredients in mock data
        dish_ids_with_ingredients = [101, 102, 103, 201, 202, 301, 401]
        results = []
        
        for dish_id in dish_ids_with_ingredients:
            success, response = self.run_test(
                f"Get Ingredients for Dish {dish_id}", 
                "GET", 
                f"dishes/{dish_id}/ingredients", 
                200
            )
            results.append(success)
            
            if success and response:
                # Verify response structure
                if "dish" not in response or "ingredients" not in response:
                    print(f"❌ Invalid ingredients response structure for dish {dish_id}")
                    return False
                    
        # Test with non-existent dish
        success, _ = self.run_test(
            "Get Ingredients for Non-existent Dish", 
            "GET", 
            "dishes/9999/ingredients", 
            404
        )
        results.append(success)
        
        return all(results)

    def test_user_selections(self):
        """Test user selection operations"""
        results = []
        
        # Test getting empty selections initially
        success, response = self.run_test(
            "Get Initial Selections", 
            "GET", 
            f"selections/{self.user_id}", 
            200
        )
        results.append(success)
        
        if success and response:
            if response.get("total_count", 0) != 0:
                print("❌ Initial selections should be empty")
                return False
        
        # Test adding a selection
        success, response = self.run_test(
            "Add Selection", 
            "POST", 
            f"selections/{self.user_id}", 
            200,
            data={"dish_id": 101, "quantity": 1}
        )
        results.append(success)
        
        # Test getting selections after adding
        success, response = self.run_test(
            "Get Selections After Adding", 
            "GET", 
            f"selections/{self.user_id}", 
            200
        )
        results.append(success)
        
        if success and response:
            if response.get("total_count", 0) != 1:
                print(f"❌ Expected 1 selection, got {response.get('total_count', 0)}")
                return False
        
        # Test adding another selection
        success, response = self.run_test(
            "Add Another Selection", 
            "POST", 
            f"selections/{self.user_id}", 
            200,
            data={"dish_id": 201, "quantity": 1}
        )
        results.append(success)
        
        # Test removing a selection
        success, response = self.run_test(
            "Remove Selection", 
            "DELETE", 
            f"selections/{self.user_id}/101", 
            200
        )
        results.append(success)
        
        # Test final selections count
        success, response = self.run_test(
            "Get Final Selections", 
            "GET", 
            f"selections/{self.user_id}", 
            200
        )
        results.append(success)
        
        if success and response:
            if response.get("total_count", 0) != 1:
                print(f"❌ Expected 1 selection after removal, got {response.get('total_count', 0)}")
                return False
        
        return all(results)

    def test_combined_filters(self):
        """Test combining multiple filters"""
        success, response = self.run_test(
            "Combined Filters (STARTER + VEG + Search)", 
            "GET", 
            "dishes", 
            200,
            params={"meal_type": "STARTER", "dish_type": "VEG", "search": "Paneer"}
        )
        
        if success and response:
            for dish in response:
                if (dish.get("mealType") != "STARTER" or 
                    dish.get("type") != "VEG" or 
                    "paneer" not in dish.get("name", "").lower()):
                    print(f"❌ Combined filter failed for dish: {dish.get('name')}")
                    return False
        
        return success

def main():
    print("🚀 Starting Party Menu Selection API Tests")
    print("=" * 60)
    
    tester = PartyMenuAPITester()
    
    # Run all tests
    test_methods = [
        tester.test_root_endpoint,
        tester.test_get_all_dishes,
        tester.test_get_dishes_by_meal_type,
        tester.test_get_dishes_by_type,
        tester.test_search_dishes,
        tester.test_get_meal_types,
        tester.test_dish_ingredients,
        tester.test_user_selections,
        tester.test_combined_filters
    ]
    
    for test_method in test_methods:
        try:
            test_method()
        except Exception as e:
            print(f"❌ Test {test_method.__name__} failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Backend API is working correctly.")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())