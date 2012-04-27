package zing.jarvis;

import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * Domokun v2.0
 * Based on Voce example by Tyler Streeter
 * Web: voce.sourceforge.net
 *
 * @author Jiraiya
 */
public class Domokun
{
	public static void main(String[] argv)
	{
		zing.jarvis.SpeechInterface.init("../../../lib", true, false, "", "");

		zing.jarvis.SpeechInterface.synthesize("This is a speech synthesis test.");
		zing.jarvis.SpeechInterface.synthesize("Type a message to hear it spoken " 
			+ "aloud.");

		System.out.println("This is a speech synthesis test.  " 
			+ "Type a message to hear it spoken aloud.");
		System.out.println("Type 's' + 'enter' to make the "
			+ "synthesizer stop speaking.  Type 'q' + 'enter' to quit.");

		BufferedReader console = 
			new BufferedReader(new InputStreamReader(System.in));

		try
		{
			String s = "";
			while (!s.equals("q"))
			{
				// Read a line from keyboard.
				s = console.readLine();

				if (s.equals("s"))
				{
					zing.jarvis.SpeechInterface.stopSynthesizing();
				}
				else
				{
					// Speak what was typed.
					zing.jarvis.SpeechInterface.synthesize(s);
				}
			}
		}
		catch (java.io.IOException ioe)
		{
			System.out.println( "IO error:" + ioe );
		}

		zing.jarvis.SpeechInterface.destroy();
		System.exit(0);
	}
}

