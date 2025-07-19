import React from 'react';
import { View, Text, StyleSheet, Dimensions, StatusBar, TouchableOpacity } from 'react-native';

const { width, height } = Dimensions.get('window');

const ProfileScreen = () => {
  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <View style={styles.content}>
        <Text style={styles.title}>Profile</Text>
        
        <View style={styles.profileSection}>
          <View style={styles.avatarPlaceholder}>
            <Text style={styles.avatarText}>Photo</Text>
          </View>
          <Text style={styles.name}>Your Name</Text>
          <Text style={styles.email}>your.email@example.com</Text>
        </View>
        
        <View style={styles.optionsSection}>
          <TouchableOpacity style={styles.option}>
            <Text style={styles.optionText}>Edit Profile</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.option}>
            <Text style={styles.optionText}>Answer Questions</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.option}>
            <Text style={styles.optionText}>Settings</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.option}>
            <Text style={styles.optionText}>Logout</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: width,
    height: height + 50,
    backgroundColor: '#FFF0F5',
    paddingTop: 50,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 30,
    textAlign: 'center',
  },
  profileSection: {
    alignItems: 'center',
    marginBottom: 40,
  },
  avatarPlaceholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#FFE4E1',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#FFB7C5',
    borderStyle: 'dashed',
  },
  avatarText: {
    fontSize: 16,
    color: '#FFB7C5',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 5,
  },
  email: {
    fontSize: 16,
    color: '#FFB7C5',
  },
  optionsSection: {
    flex: 1,
  },
  option: {
    backgroundColor: '#FFE4E1',
    paddingVertical: 16,
    paddingHorizontal: 20,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#FFB7C5',
  },
  optionText: {
    fontSize: 18,
    color: '#FF69B4',
    fontWeight: '500',
  },
});

export default ProfileScreen; 