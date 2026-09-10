import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';

import { COLORS } from './constants/theme';
import LanguageScreen  from './screens/LanguageScreen';
import HomeScreen      from './screens/HomeScreen';
import RecordScreen    from './screens/RecordScreen';
import ReviewScreen    from './screens/ReviewScreen';
import ProductsScreen  from './screens/ProductsScreen';
import ExportScreen    from './screens/ExportScreen';

const Stack = createStackNavigator();
const Tab   = createBottomTabNavigator();

// ── Bottom tab navigator (main app) ──────────────────────────
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor:   COLORS.primary,
        tabBarInactiveTintColor: '#999999',
        tabBarStyle: {
          backgroundColor: '#FFFFFF',
          borderTopColor: '#EEEEEE',
          paddingBottom: 8,
          paddingTop: 6,
          height: 64,
        },
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
        tabBarIcon: ({ focused, color }) => {
          const icons: Record<string, [string, string]> = {
            Home:     ['home',         'home-outline'],
            Record:   ['mic-circle',   'mic-circle-outline'],
            Products: ['grid',         'grid-outline'],
            Export:   ['cloud-upload', 'cloud-upload-outline'],
          };
          const [active, inactive] = icons[route.name] ?? ['ellipse', 'ellipse-outline'];
          return (
            <Ionicons
              name={(focused ? active : inactive) as any}
              size={24}
              color={color}
            />
          );
        },
      })}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'होम' }}
      />
      <Tab.Screen
        name="Record"
        component={RecordScreen}
        options={{ title: 'नया' }}
      />
      <Tab.Screen
        name="Products"
        component={ProductsScreen}
        options={{ title: 'उत्पाद' }}
      />
      <Tab.Screen
        name="Export"
        component={ExportScreen}
        options={{ title: 'निर्यात' }}
      />
    </Tab.Navigator>
  );
}

// ── Root stack (language select → main app + modal screens) ──
export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator
        initialRouteName="Language"
        screenOptions={{ headerShown: false }}
      >
        {/* Onboarding */}
        <Stack.Screen name="Language" component={LanguageScreen} />

        {/* Main tabs */}
        <Stack.Screen name="Main" component={MainTabs} />

        {/* Modal screens pushed over tabs */}
        <Stack.Screen
          name="Review"
          component={ReviewScreen}
          options={{
            headerShown: true,
            title: 'Review & Price',
            headerTintColor: COLORS.primary,
            headerStyle: { backgroundColor: COLORS.white },
            headerBackTitle: 'Back',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
