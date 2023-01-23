package GUI;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.stage.Stage;

public class QualityController implements Initializable {
	public static Stage primaryStage;

	@FXML
	private Button homeBtn;

	@FXML
	private Button backBtn;
	
    @FXML
    private Label varStd2;

    @FXML
    private Label varStd1;
    
	@FXML
	private ImageView simpleStrategy;

	@FXML
	private ImageView learningStrategy;

	@FXML
	void BackStep(ActionEvent event) {
		SetStrategyController setStrategyController = new SetStrategyController();
		setStrategyController.start(primaryStage);

	}

	@FXML
	void HomeStep(ActionEvent event) throws Exception {
		EnterParamsController enterParamsController = new EnterParamsController();
		enterParamsController.start(primaryStage);
	}

	public void start(Stage primaryStage) {
		QualityController.primaryStage = primaryStage;
		try {
			SimulatedTrafficController.primaryStage = primaryStage;
			Parent root;
			root = FXMLLoader.load(getClass().getResource("QualityEstimation.fxml"));
			Scene scene = new Scene(root);
			SimulatedTrafficController.primaryStage.setScene(scene);
			SimulatedTrafficController.primaryStage.setTitle("Quality Estimation");
			SimulatedTrafficController.primaryStage.show();
			SimulatedTrafficController.primaryStage.setOnCloseRequest(event -> {
				System.exit(0);
			});
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub
		FileInputStream imgResult = null;
		FileInputStream imgResult2 = null;

		try {

			imgResult = new FileInputStream("C:\\Users\\franc\\eclipse-workspace\\Phase2\\src\\GUI\\tests result.png");
			imgResult2 = new FileInputStream("C:\\Users\\franc\\eclipse-workspace\\Phase2\\src\\GUI\\tests result2.png");

		} catch (FileNotFoundException e) {

			e.printStackTrace();
		}
		Image image = new Image(imgResult);
		simpleStrategy.setImage(image);
		simpleStrategy.setLayoutX(90);
		simpleStrategy.setLayoutY(120);
		simpleStrategy.setFitWidth(450);
		simpleStrategy.setFitHeight(450);
		// ViewImg.setVisible(true);
		simpleStrategy.setPreserveRatio(true);
		
		
		Image image2 = new Image(imgResult2);
		learningStrategy.setImage(image2);
		learningStrategy.setLayoutX(570);
		learningStrategy.setLayoutY(120);
		learningStrategy.setFitWidth(450);
		learningStrategy.setFitHeight(450);
		// ViewImg.setVisible(true);
		learningStrategy.setPreserveRatio(true);
		
		
		try {

            File file = new File("C:\\Users\\franc\\eclipse-workspace\\Phase2\\varResult1.txt");
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);
            String line;
            while ((line = br.readLine()) != null) {
            	varStd1.setText(line);
            }
            br.close();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
		

		try {

            File file = new File("C:\\Users\\franc\\eclipse-workspace\\Phase2\\varResult2.txt");
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);
            String line;
            while ((line = br.readLine()) != null) {
            	varStd2.setText(line);
            }
            br.close();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

	}

}
