import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {

    public static void main(String[] args) {

        try {

            BufferedReader br = new BufferedReader(
                    new InputStreamReader(System.in)
            );

           
            System.out.println(" AI-Based Fake News Detection System ");
            

            System.out.print("\nEnter News Text: ");

            String input = br.readLine();

            ProcessBuilder pb = new ProcessBuilder(
                    "python",
                    "python/predict.py",
                    input
            );

            Process process = pb.start();

            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream())
            );

            String output = reader.readLine();

            if (output == null) {
                System.out.println("No output received from Python");
                return;
            }

            String[] result = output.split("\\|");

            String prediction = result[0];
            String confidence = result[1];
            String explanation = result[2];

            System.out.println("\n RESULT ");

            System.out.println("Prediction : " + prediction.toUpperCase());
            System.out.println("Confidence : " + confidence + "%");
            System.out.println("Explanation: " + explanation);

            if (prediction.equalsIgnoreCase("fake")) {
                System.out.println("\nWARNING: This news may be fake or misleading.");
            }
            else {
                System.out.println("\nThis news appears reliable.");
            }

        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}