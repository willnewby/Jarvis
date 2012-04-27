package zing.jarvis;

import org.apache.log4j.Logger;

import edu.cmu.sphinx.frontend.util.Microphone;
import edu.cmu.sphinx.recognizer.Recognizer;
import edu.cmu.sphinx.result.Result;
import edu.cmu.sphinx.util.props.ConfigurationManager;

/**
 * uses the Sphinx-4 endpointer, which automatically segments incoming audio
 * into utterances and silences.
 */
public class Jarvis {

	private static final Logger logger = Logger.getLogger(Jarvis.class);

	public static void main(String[] args) {
		ConfigurationManager cm;

		if (args.length > 0) {
			cm = new ConfigurationManager(args[0]);
		} else {
			cm = new ConfigurationManager("config/sphinx.config.xml");
		}

		Recognizer recognizer = (Recognizer) cm.lookup("recognizer");
		recognizer.allocate();

		// start the microphone or exit if the programm if this is not possible
		Microphone microphone = (Microphone) cm.lookup("microphone");
		if (!microphone.startRecording()) {
			logger.error("Cannot start microphone.");
			recognizer.deallocate();
			System.exit(1);
		}

		logger.info("Jarvis online. Good morning, sir.");
		
		// loop the recognition until the programm exits.
		while (true) {
			Result result = recognizer.recognize();

			if (result != null) {
				String resultText = result.getBestFinalResultNoFiller();

				if (resultText.equals("shutdown")) {
					logger.info("Shutting down.");
					break;
				}

				logger.info("Command received: '" + resultText + "'.");
			}
		}

		recognizer.deallocate();
		System.exit(0);
	}
}
