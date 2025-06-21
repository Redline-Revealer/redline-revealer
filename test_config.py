#!/usr/bin/env python3
"""
Simple validation script to test .env configuration for Redline Revealer
"""
import os
import sys
from dotenv import load_dotenv

def test_env_config():
    print("🔍 Testing .env configuration for Redline Revealer...")
    
    # Load environment variables
    load_dotenv()
    
    # Required variables for the app to function
    required_vars = {
        'AZURE_OPENAI_KEY': 'Azure OpenAI API Key',
        'AZURE_OPENAI_ENDPOINT': 'Azure OpenAI Endpoint URL', 
        'AZURE_OPENAI_API_VERSION': 'Azure OpenAI API Version',
        'AZURE_OPENAI_CHAT_DEPLOYMENT': 'Azure OpenAI Chat Model Deployment',
        'AZURE_OPENAI_EMBEDDING_DEPLOYMENT': 'Azure OpenAI Embedding Model Deployment',
        'AZURE_OPENAI_EMBEDDING_MODEL': 'Azure OpenAI Embedding Model Name',
        'AZURE_SEARCH_ENDPOINT': 'Azure Search Service Endpoint',
        'AZURE_SEARCH_KEY': 'Azure Search Service Key',
        'AZURE_STORAGE_CONNECTION_STRING': 'Azure Storage Connection String',
        'AZURE_BLOB_CONN_STR': 'Azure Blob Storage Connection String',
        'AZURE_BLOB_CONTAINER': 'Azure Blob Container Name',
        'AZURE_BLOB_BASE_URL': 'Azure Blob Base URL',
        'AZURE_MAPS_SUBSCRIPTION_KEY': 'Azure Maps Subscription Key',
        'AZURE_MAPS_ENDPOINT': 'Azure Maps Endpoint URL'
    }
    
    # Check each variable
    missing_vars = []
    configured_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value.strip() and not value.startswith('your-'):
            configured_vars.append(f"✅ {var}: {description}")
        else:
            missing_vars.append(f"❌ {var}: {description}")
    
    # Print results
    print(f"\n📊 Configuration Status:")
    print(f"✅ Configured: {len(configured_vars)}")
    print(f"❌ Missing/Invalid: {len(missing_vars)}")
    
    if configured_vars:
        print(f"\n✅ Properly Configured Variables:")
        for var in configured_vars:
            print(f"   {var}")
    
    if missing_vars:
        print(f"\n❌ Missing or Invalid Variables:")
        for var in missing_vars:
            print(f"   {var}")
        print(f"\n💡 Please update these variables in your .env file")
    
    # Test basic imports
    print(f"\n🧪 Testing Module Imports...")
    try:
        from modules import welcome
        print("✅ Welcome module import successful")
    except Exception as e:
        print(f"❌ Welcome module import failed: {e}")
        
    try:
        from modules import about
        print("✅ About module import successful")
    except Exception as e:
        print(f"❌ About module import failed: {e}")
        
    try:
        from modules import assistant
        print("✅ Assistant module import successful")  
    except Exception as e:
        print(f"❌ Assistant module import failed: {e}")
        
    try:
        from modules import map_page
        print("✅ Map module import successful")
    except Exception as e:
        print(f"❌ Map module import failed: {e}")
    
    # Test legal agent initialization
    print(f"\n🤖 Testing Legal Agent...")
    try:
        from agent.legal_agent import client, llm, retriever
        
        if client:
            print("✅ Azure OpenAI client initialized")
        else:
            print("⚠️ Azure OpenAI client not initialized (check credentials)")
            
        if llm:
            print("✅ Language model initialized") 
        else:
            print("⚠️ Language model not initialized (check credentials)")
            
        if retriever:
            print("✅ Document retriever initialized")
        else:
            print("⚠️ Document retriever not initialized (FAISS index may be missing)")
            
    except Exception as e:
        print(f"❌ Legal agent initialization failed: {e}")
    
    print(f"\n🎯 Configuration Test Complete!")
    
    if not missing_vars:
        print("🚀 Your configuration looks good! The app should run smoothly.")
        return True
    else:
        print("⚠️ Please fix the missing/invalid variables before running the app.")
        return False

if __name__ == "__main__":
    success = test_env_config()
    sys.exit(0 if success else 1)
