import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';

import { COLORS } from './constants/theme';
import LanguageScreen from './screens/LanguageScreen';
import HomeScreen from './screens/HomeScreen';
import RecordScreen from './screens/RecordScreen';
import ReviewScreen from './screens/ReviewScreen';
import ProductsScreen from './screens/ProductsScreen';
import ExportScreen from './screens/ExportScreen';
import ProductDetailScreen from './screens/ProductDetailScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      initialRouteName="Home"
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: '#8F8F8F',
        tabBarStyle: {
          backgroundColor: '#F7F6F4',
          borderTopWidth: 0,
          height: 70,
          paddingBottom: 10,
          paddingTop: 8,
          elevation: 0,
          shadowOpacity: 0,
        },
        tabBarLabelStyle: {
          fontSize: 10,
          fontWeight: '600',
          marginTop: 2,
        },
        tabBarIcon: ({ focused, color }) => {
          const icons: Record<string, [string, string]> = {
            Home: ['home', 'home-outline'],
            Products: ['cube', 'cube-outline'],
            Market: ['storefront', 'storefront-outline'],
            Profile: ['person', 'person-outline'],
          };
          const [active, inactive] = icons[route.name] ?? ['ellipse', 'ellipse-outline'];
          return <Ionicons size={22} color={color} name={(focused ? active : inactive) as any} />;
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: 'Home' }} />
      <Tab.Screen name="Products" component={ProductsScreen} options={{ title: 'Products' }} />
      <Tab.Screen name="Market" component={ExportScreen} options={{ title: 'Market' }} />
      <Tab.Screen name="Profile" component={ProductsScreen} options={{ title: 'Profile' }} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="dark" />
      <Stack.Navigator
        initialRouteName="Language"
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name="Language" component={LanguageScreen} />
        <Stack.Screen name="Main" component={MainTabs} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Review" component={ReviewScreen} />
        <Stack.Screen name="Record" component={RecordScreen} />
        <Stack.Screen name="Products" component={ProductsScreen} />
        <Stack.Screen name="Market" component={ExportScreen} />
        <Stack.Screen name="ProductDetail" component={ProductDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
