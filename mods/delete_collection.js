const admin = require('firebase-admin');


const cred = admin.credential.cert(JSON.parse(process.env.GOOGLE_CRED));
const app = admin.initializeApp({
    credential: cred
});
db = admin.firestore(app);
const ref = db.collection(process.argv[2]);
delete_collection(ref);

function delete_collection(collRef){
    const promises = [];

    return collRef.get()
        .then(qs => {
            qs.forEach(docSnapshot => {
                promises.push(docSnapshot.ref.delete());
            });
            return Promise.all(promises);
        })
        .catch(error => {
            console.log(error);
            return false;
        });
}

