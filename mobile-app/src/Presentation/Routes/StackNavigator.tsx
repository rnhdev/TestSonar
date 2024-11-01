import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import {HomeScreen} from '../Screens/Home/HomeScreen';
import {LoginScreen} from '../Screens/Auth/LoginScreen';
import {RegisterScreen} from '../Screens/Auth/RegisterScreen';
import {IncidentReportScreen} from '../Screens/Incidents/IncidentReportScreen';
import {ResumeIncidentScreen} from '../Screens/Incidents/ResumeIncidentScreen';
import {SettingsIncidentScreen} from '../Screens/Incidents/SettingsIncidentScreen';
import TabNavigator from './TabNavigator';
import {Animated} from 'react-native';

export type RootStackParamList = {
  LoginScreen: undefined;
  RegisterScreen: undefined;
  HomeScreen: undefined;
  IncidentReportScreen: undefined;
  ResumeIncidentScreen: undefined;
  SettingsIncidentScreen: undefined;
  Main: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

type FadeAnimationProps = {
  current: {
    progress: Animated.AnimatedInterpolation<number>;
  };
};
const fadeAnimation = ({current}: FadeAnimationProps) => ({
  cardStyle: {
    opacity: current.progress,
  },
});

export const StackNavigator = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        cardStyleInterpolator: fadeAnimation,
      }}
      initialRouteName="LoginScreen">
      <Stack.Screen
        options={{
          headerShown: false,
        }}
        name="LoginScreen"
        component={LoginScreen}
      />
      <Stack.Screen
        options={{
          headerShown: false,
        }}
        name="RegisterScreen"
        component={RegisterScreen}
      />
      <Stack.Screen
        options={{
          headerShown: false,
        }}
        name="HomeScreen"
        component={HomeScreen}
      />
      <Stack.Screen
        name="Main"
        component={TabNavigator}
        options={{headerShown: false}}
      />
      <Stack.Screen
        options={{
          headerShown: false,
        }}
        name="IncidentReportScreen"
        component={IncidentReportScreen}
      />
      <Stack.Screen
        options={{
          headerShown: false,
        }}
        name="ResumeIncidentScreen"
        component={ResumeIncidentScreen}
      />
      <Stack.Screen
        options={{
          headerShown: false,
        }}
        name="SettingsIncidentScreen"
        component={SettingsIncidentScreen}
      />
    </Stack.Navigator>
  );
};
