package zing.jarvis;

import org.apache.log4j.Logger;

import edu.cmu.sphinx.frontend.util.Microphone;
import edu.cmu.sphinx.recognizer.Recognizer;
import edu.cmu.sphinx.result.Result;
import edu.cmu.sphinx.util.props.ConfigurationManager;

/**
 * Uses the Sphinx-4 endpointer, which automatically segments incoming audio into utterances and
 * silences.
 * 
 * @author AJ Minich (aj@ajminich.com)
 */
public class Jarvis {

  private static final Logger logger = Logger.getLogger(Jarvis.class);

  // Constants
  public static final String CONFIG_FILE = "src/resources/sphinx.config.xml";

  // Private members
  private final ConfigurationManager cm;
  private Recognizer recognizer;

  public static void main(String[] args) {
    
    String configFile = (args.length > 0) ? args[0] : CONFIG_FILE;
    
    Jarvis jarvis;
    try {
      jarvis = new Jarvis(configFile);
    } catch (Exception ex) {
      logger.error(ex);
      return;
    }

    // loop recognition until the user gives the 'shutdown' command.
    while (true) {

      String command = jarvis.getCommand();

      if (command.equals("shutdown")) {
        logger.info("Shutting down.");
        break;
      }

      logger.info("Command received: '" + command + "'.");
    }
    
    System.exit(0);
  }

  public Jarvis(String sphinxConfigFile) throws Exception {

    cm = new ConfigurationManager(sphinxConfigFile);

    recognizer = (Recognizer) cm.lookup("recognizer");
    recognizer.allocate();

    // start the microphone or exit if the program if this is not possible
    Microphone microphone = (Microphone) cm.lookup("microphone");
    if (!microphone.startRecording()) {
      recognizer.deallocate();
      throw new Exception("Cannot start microphone.");
    }

    logger.info("Jarvis online. Good morning, sir.");
  }

  public String getCommand() {

    Result result = null;

    // continue recognition until the user gives a recognized command
    while (result == null) {
      result = recognizer.recognize();
    }

    String resultText = result.getBestFinalResultNoFiller();
    return resultText;
  }

  public void shutdown() {
    recognizer.deallocate();
  }
}
