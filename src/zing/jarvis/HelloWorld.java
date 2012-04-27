package zing.jarvis;

import javax.speech.*;
import javax.speech.recognition.*;
import java.io.FileReader;
import java.util.Locale;

public class HelloWorld extends ResultAdapter {
	static Recognizer rec;

	// Receives RESULT_ACCEPTED event: print it, clean up, exit
	public void resultAccepted(ResultEvent e) {
		Result r = (Result) (e.getSource());
		ResultToken tokens[] = r.getBestTokens();

		for (int i = 0; i < tokens.length; i++)
			System.out.print(tokens[i].getSpokenText() + " ");
		System.out.println();

		// Deallocate the recognizer and exit
		try {
			rec.deallocate();
		} catch (EngineException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (EngineStateError e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		System.exit(0);
	}

	public static void main(String args[]) {
		try {
			// Create a recognizer that supports English.
			rec = Central.createRecognizer(new EngineModeDesc(Locale.ENGLISH));

			// Start up the recognizer
			rec.allocate();

			// Load the grammar from a file, and enable it
			FileReader reader = new FileReader(args[0]);
			RuleGrammar gram = rec.loadJSGF(reader);
			gram.setEnabled(true);

			// Add the listener to get results
			rec.addResultListener(new HelloWorld());

			// Commit the grammar
			rec.commitChanges();

			// Request focus and start listening
			rec.requestFocus();
			rec.resume();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
