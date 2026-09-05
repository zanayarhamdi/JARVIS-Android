import sys
from pathlib import Path
from datetime import datetime
from core.logger import create_logger
from core.config import get_config
from agent.agent_core import JARVISAgent
from memory.memory_manager import get_memory_manager

logger = create_logger("JARVIS_MAIN")

def initialize_jarvis():
    """Initialize JARVIS system"""
    logger.info("="*50)
    logger.info("Initializing JARVIS Android")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("="*50)
    
    # Load configuration
    config = get_config()
    logger.info(f"JARVIS Version: {config.get('jarvis.version')}")
    logger.info(f"Configuration loaded from: config/")
    
    # Initialize memory
    memory = get_memory_manager()
    logger.info("Memory system initialized")
    
    # Initialize agent
    agent = JARVISAgent()
    logger.info("Agent core initialized")
    
    return agent, config, memory

def main():
    """Main JARVIS entry point"""
    try:
        agent, config, memory = initialize_jarvis()
        
        logger.info("\nJARVIS initialized successfully")
        logger.info(f"Ready to process input...\n")
        
        # Interactive loop
        print(f"\n{config.get('jarvis.name')} v{config.get('jarvis.version')}")
        print("="*50)
        print(f"Ready. Type 'exit' to quit.\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'خروج']:
                    print(f"{config.get('jarvis.name')}: خدا حافظ.")
                    logger.info("JARVIS shutdown")
                    break
                
                # Process input
                result = agent.process_input(user_input)
                
                # Display response
                if result.get('success'):
                    response = result.get('response', 'انجام شد.')
                    print(f"\n{config.get('jarvis.name')}: {response}\n")
                elif result.get('requires_clarification'):
                    print(f"\n{config.get('jarvis.name')}: {result.get('clarification_question')}\n")
                elif result.get('requires_confirmation'):
                    print(f"\n{config.get('jarvis.name')}: {result.get('confirmation_message')}")
                    confirmation = input("You (yes/no): ").strip().lower()
                    if confirmation in ['yes', 'y']:
                        print(f"{config.get('jarvis.name')}: اوکی، شروع می‌کنم.\n")
                    else:
                        print(f"{config.get('jarvis.name')}: منصرف شدم.\n")
                else:
                    error_msg = result.get('response', result.get('error', 'خطای نامشخص'))
                    print(f"\n{config.get('jarvis.name')}: {error_msg}\n")
            
            except KeyboardInterrupt:
                print(f"\n\n{config.get('jarvis.name')}: خدا حافظ.")
                logger.info("JARVIS interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"Error: {e}\n")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
